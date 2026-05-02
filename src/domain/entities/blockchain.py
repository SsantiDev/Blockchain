from typing import List, Optional
from .block import Block
from .transaction import Transaction
from ..interfaces.cryptography_service import CryptographyService

class Blockchain:
    """
    Core Domain Logic for the Blockchain.
    Independent of persistence, networking, and specific crypto implementations.
    """
    def __init__(self, crypto_service: CryptographyService, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.crypto_service = crypto_service
        self.nodes = set()
        
        # Genesis block creation is part of domain initialization
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_tx = Transaction("SYSTEM", "GENESIS_DOCUMENT", {"note": "Genesis Block"})
        genesis_block = Block(0, [genesis_tx], "0")
        genesis_block.hash = self.crypto_service.calculate_hash(genesis_block)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        if not transaction.signature or not self.crypto_service.verify_signature(
            transaction.owner, transaction.signature, self.crypto_service.calculate_hash(transaction)
        ):
            if transaction.owner != "SYSTEM":
                raise ValueError("Invalid transaction signature")
        
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str) -> Block:
        # Create reward transaction
        reward_tx = Transaction("SYSTEM", "REWARD", {"note": f"Reward for {miner_address}"})
        self.pending_transactions.append(reward_tx)
        
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=previous_block.hash
        )
        
        # Proof of Work logic
        target = "0" * self.difficulty
        while True:
            new_block.hash = self.crypto_service.calculate_hash(new_block)
            if new_block.hash.startswith(target):
                break
            new_block.nonce += 1
            
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self, chain: List[Block]) -> bool:
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i-1]
            
            # Verify hash
            if current.hash != self.crypto_service.calculate_hash(current):
                return False
                
            # Verify link
            if current.previous_hash != previous.hash:
                return False
        return True
