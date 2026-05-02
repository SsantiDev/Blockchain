from src.domain.entities.blockchain import Blockchain
from src.domain.entities.transaction import Transaction
from src.infrastructure.cryptography.ecdsa_service import ECDSAService
import sys

def test_domain_logic():
    print("\n🔍 Testing Clean Architecture Domain Logic...")
    
    # 1. Setup Infrastructure (Injected)
    crypto = ECDSAService()
    
    # 2. Initialize Domain
    blockchain = Blockchain(crypto_service=crypto, difficulty=3)
    print(f"Genesis Block Hash: {blockchain.chain[0].hash}")

    # 3. Create Identity
    keys = crypto.generate_key_pair()
    owner = keys["public_key_hex"]
    
    # 4. Create Transaction
    tx = Transaction(owner, "test_document_hash", {"file": "test.txt"})
    
    # Sign using the service
    tx_hash = crypto.calculate_hash(tx)
    tx.signature = crypto.sign_data(tx_hash, keys["private_key"])
    
    # 5. Add and Mine
    try:
        blockchain.add_transaction(tx)
        print("✅ Transaction signed and validated correctly.")
        
        new_block = blockchain.mine_pending_transactions(owner)
        print(f"✅ Block {new_block.index} mined with hash: {new_block.hash}")
        
        # 6. Final check
        if blockchain.is_chain_valid(blockchain.chain):
            print("🏆 Blockchain Integrity Verified!")
        else:
            print("❌ Blockchain Integrity Failed!")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_domain_logic()
