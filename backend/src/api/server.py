from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import os
import shutil
import uuid

from src.domain.entities.blockchain import Blockchain
from src.infrastructure.cryptography.ecdsa_service import ECDSAService
from src.infrastructure.persistence.sql_repository import SQLBlockchainRepository
from src.infrastructure.persistence.database import SessionLocal, get_db
from src.infrastructure.persistence.json_repository import JSONBlockchainRepository
from src.infrastructure.persistence.models import User as UserModel, TransactionModel
from src.application.use_cases.notary_service import NotaryService
from src.application.services.auth_service import AuthService
from src.infrastructure.services.pdf_service import PDFCertificateGenerator
from src.api.schemas.auth_schemas import UserRegister, UserLogin, Token, UserResponse

app = FastAPI(title="NotaryChain Commercial API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection
crypto_service = ECDSAService()
db = SessionLocal()
repository = SQLBlockchainRepository(db)
pdf_generator = PDFCertificateGenerator()

# Migration Logic: JSON -> SQL (One time)
JSON_PATH = "blockchain.json"
if not os.path.exists(JSON_PATH) and os.path.exists("backend/blockchain.json"):
    JSON_PATH = "backend/blockchain.json"

if os.path.exists(JSON_PATH):
    print(f"📦 Migrating legacy JSON data from {JSON_PATH} to SQL...")
    try:
        old_repo = JSONBlockchainRepository(file_path=JSON_PATH)
        old_chain = old_repo.load_chain()
        if old_chain:
            repository.save_chain(old_chain)
            os.rename(JSON_PATH, JSON_PATH + ".bak")
            print(f"✅ Migration successful. {JSON_PATH} renamed to '.bak'")
    except Exception as e:
        print(f"⚠️ Migration failed: {e}")

blockchain = Blockchain(crypto_service=crypto_service)
notary_service = NotaryService(blockchain, repository, crypto_service)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Dependencies ---

def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    email = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

# --- Auth Endpoints ---

@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserRegister, db: SessionLocal = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    hashed_pwd = AuthService.get_password_hash(user_data.password)
    new_user = UserModel(
        email=user_data.email,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name,
        wallet_address=user_data.wallet_address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=Token)
def login(credentials: UserLogin, db: SessionLocal = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == credentials.email).first()
    if not user or not AuthService.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

# --- Notary Endpoints ---
def read_root():
    return {"message": "Welcome to NotaryChain Commercial API", "status": "active"}

@app.post("/notarize")
async def notarize_document(
    owner_address: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    # Inject current DB session into repository for this request
    repository.set_db(db)
    
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.abspath(temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 1. Generate real keys for the transaction
        keys = crypto_service.generate_key_pair() 
        public_key = keys["public_key_hex"]
        private_key = keys["private_key"]
        
        # 2. Notarize with user context in metadata
        result = notary_service.notarize_file(
            temp_path, 
            public_key, 
            private_key, 
            {
                "description": description,
                "display_address": owner_address,
                "original_filename": file.filename,
                "user_id": current_user.id # This will be used by the SQL repo
            }
        )
        
        result["owner"] = owner_address
        return result
        
    except Exception as e:
        print(f"❌ Error in /notarize: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/my-notarizations")
def get_user_history(
    current_user: UserModel = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    # We query the TransactionModel table directly for speed
    history = db.query(TransactionModel).filter(TransactionModel.user_id == current_user.id).all()
    
    return [
        {
            "timestamp": t.timestamp,
            "document_hash": t.document_hash,
            "metadata": t.metadata_json,
            "owner": t.owner_address,
            "signature": t.signature
        } for t in history
    ]

@app.get("/notarizations/{document_hash}/certificate")
def download_certificate(
    document_hash: str,
    db: SessionLocal = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Search for the transaction in the DB associated with the user
    tx = db.query(TransactionModel).filter(
        TransactionModel.document_hash == document_hash,
        TransactionModel.user_id == current_user.id
    ).first()
    
    if not tx:
        raise HTTPException(status_code=404, detail="Certificado no encontrado o acceso denegado")
    
    tx_data = {
        "owner": tx.owner_address,
        "timestamp": tx.timestamp,
        "document_hash": tx.document_hash,
        "metadata": tx.metadata_json,
        "signature": tx.signature
    }
    
    pdf_stream = pdf_generator.generate_certificate(tx_data)
    
    filename = f"certificado_{document_hash[:8]}.pdf"
    return StreamingResponse(
        pdf_stream, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    temp_filename = f"verify_{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.abspath(temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        result = notary_service.verify_document(temp_path)
        return result
    except Exception as e:
        print(f"❌ Error in /verify: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/chain")
def get_chain():
    return {
        "length": len(blockchain.chain),
        "chain": [b.__dict__ for b in blockchain.chain]
    }
