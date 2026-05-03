from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
import uuid

from src.domain.entities.blockchain import Blockchain
from src.infrastructure.cryptography.ecdsa_service import ECDSAService
from src.infrastructure.persistence.json_repository import JSONBlockchainRepository
from src.application.use_cases.notary_service import NotaryService

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
repository = JSONBlockchainRepository()
blockchain = Blockchain(crypto_service=crypto_service)
notary_service = NotaryService(blockchain, repository, crypto_service)

@app.get("/")
def read_root():
    return {"message": "Welcome to NotaryChain Commercial API", "status": "active"}

@app.post("/notarize")
async def notarize_document(
    owner_address: str = Form(...),
    private_key_hex: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...)
):
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.abspath(temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 1. Generate real keys for the transaction
        keys = crypto_service.generate_key_pair() 
        public_key = keys["public_key_hex"]
        private_key = keys["private_key"]
        
        # 2. Notarize using the Public Key as the official owner for signature verification
        # But we store the display address in metadata
        result = notary_service.notarize_file(
            temp_path, 
            public_key, 
            private_key, 
            {
                "description": description,
                "display_address": owner_address,
                "original_filename": file.filename
            }
        )
        
        # 3. Return the display address to the frontend for the certificate
        result["owner"] = owner_address
        return result
        
    except Exception as e:
        print(f"❌ Error in /notarize: {str(e)}")
        # If it's a value error (like the signature one), return it clearly
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

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
