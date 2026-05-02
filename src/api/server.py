from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from typing import List, Optional
import os
import shutil

from src.domain.entities.blockchain import Blockchain
from src.infrastructure.cryptography.ecdsa_service import ECDSAService
from src.infrastructure.persistence.json_repository import JSONBlockchainRepository
from src.application.use_cases.notary_service import NotaryService

app = FastAPI(title="NotaryChain Commercial API", version="2.0.0")

# Dependency Injection Setup
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
    private_key_hex: str = Form(...), # In production, this should be handled client-side or via KMS
    description: str = Form(""),
    file: UploadFile = File(...)
):
    # Temporary save file to process it
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Load private key (simplified for demo)
        # In a real app, we'd use a more secure way to handle this
        keys = crypto_service.generate_key_pair() # Dummy generation for structure demo
        # For this demo, we'll assume the provided hex is the key (logic simplified)
        
        result = notary_service.notarize_file(
            temp_path, 
            owner_address, 
            keys["private_key"], # Mocked for demo purposes
            {"description": description}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    temp_path = f"verify_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        result = notary_service.verify_document(temp_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/chain")
def get_chain():
    return {
        "length": len(blockchain.chain),
        "chain": [b.__dict__ for b in blockchain.chain] # Simplified serialization
    }
