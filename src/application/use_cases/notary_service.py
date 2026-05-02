import os
import hashlib
from typing import Dict, Any, List, Optional
from src.domain.entities.blockchain import Blockchain
from src.domain.entities.transaction import Transaction
from src.domain.interfaces.blockchain_repository import BlockchainRepository
from src.domain.interfaces.cryptography_service import CryptographyService

class NotaryService:
    """
    Application Service that coordinates Notary use cases.
    """
    def __init__(
        self, 
        blockchain: Blockchain, 
        repository: BlockchainRepository,
        crypto_service: CryptographyService
    ):
        self.blockchain = blockchain
        self.repository = repository
        self.crypto_service = crypto_service
        
        # Load existing chain if available
        existing_chain = self.repository.load_chain()
        if existing_chain:
            self.blockchain.chain = existing_chain

    def notarize_file(self, file_path: str, owner_address: str, private_key: Any, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Full workflow to notarize a physical file.
        """
        # 1. Calculate file hash
        file_hash = self._calculate_file_hash(file_path)
        
        # 2. Create and sign transaction
        metadata = metadata or {}
        metadata["filename"] = os.path.basename(file_path)
        
        transaction = Transaction(owner_address, file_hash, metadata)
        tx_hash = self.crypto_service.calculate_hash(transaction)
        transaction.signature = self.crypto_service.sign_data(tx_hash, private_key)
        
        # 3. Add to blockchain
        self.blockchain.add_transaction(transaction)
        
        # 4. Mine and Persist
        new_block = self.blockchain.mine_pending_transactions(owner_address)
        self.repository.save_chain(self.blockchain.chain)
        
        return {
            "status": "success",
            "block_index": new_block.index,
            "block_hash": new_block.hash,
            "document_hash": file_hash
        }

    def verify_document(self, file_path: str) -> Dict[str, Any]:
        """
        Verify if a document exists in the blockchain and is intact.
        """
        file_hash = self._calculate_file_hash(file_path)
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.document_hash == file_hash:
                    return {
                        "verified": True,
                        "owner": tx.owner,
                        "timestamp": tx.timestamp,
                        "metadata": tx.metadata,
                        "block": block.index
                    }
        
        return {"verified": False, "reason": "Hash not found in blockchain"}

    def _calculate_file_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
