import unittest
import os
import sys

# Setup path for Clean Architecture
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.domain.entities.blockchain import Blockchain
from src.domain.entities.transaction import Transaction
from src.infrastructure.cryptography.ecdsa_service import ECDSAService

class TestBlockchainClean(unittest.TestCase):

    def setUp(self):
        # Using the clean architecture components
        self.crypto = ECDSAService()
        self.blockchain = Blockchain(crypto_service=self.crypto, difficulty=2)
        self.keys = self.crypto.generate_key_pair()
        self.owner = self.keys["public_key_hex"]

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].transactions[0].owner, "SYSTEM")

    def test_add_valid_transaction(self):
        tx = Transaction(self.owner, "doc_hash_123", {"name": "test.pdf"})
        
        # Sign transaction
        tx_hash = self.crypto.calculate_hash(tx)
        tx.signature = self.crypto.sign_data(tx_hash, self.keys["private_key"])
        
        self.blockchain.add_transaction(tx)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
        self.assertEqual(self.blockchain.pending_transactions[0].document_hash, "doc_hash_123")

    def test_invalid_signature_fails(self):
        tx = Transaction(self.owner, "doc_hash_123")
        tx.signature = "invalid_signature"
        
        with self.assertRaises(ValueError):
            self.blockchain.add_transaction(tx)

    def test_mining_logic(self):
        tx = Transaction(self.owner, "doc_hash_mine")
        tx_hash = self.crypto.calculate_hash(tx)
        tx.signature = self.crypto.sign_data(tx_hash, self.keys["private_key"])
        
        self.blockchain.add_transaction(tx)
        self.blockchain.mine_pending_transactions(self.owner)
        
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(self.blockchain.chain[-1].index, 1)
        self.assertTrue(self.blockchain.chain[-1].hash.startswith("00"))

    def test_chain_integrity(self):
        # Add a couple of blocks
        for i in range(2):
            tx = Transaction(self.owner, f"hash_{i}")
            h = self.crypto.calculate_hash(tx)
            tx.signature = self.crypto.sign_data(h, self.keys["private_key"])
            self.blockchain.add_transaction(tx)
            self.blockchain.mine_pending_transactions(self.owner)
            
        self.assertTrue(self.blockchain.is_chain_valid(self.blockchain.chain))

        # Tamper with a block
        self.blockchain.chain[1].transactions[0].document_hash = "TAMPERED"
        self.assertFalse(self.blockchain.is_chain_valid(self.blockchain.chain))

if __name__ == '__main__':
    unittest.main()
