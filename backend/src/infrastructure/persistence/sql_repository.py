from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.interfaces.blockchain_repository import BlockchainRepository
from src.domain.entities.block import Block
from src.domain.entities.transaction import Transaction
from .models import BlockModel, TransactionModel, NodeModel
from .database import engine, Base

class SQLBlockchainRepository(BlockchainRepository):
    """
    Implementation of BlockchainRepository using SQLAlchemy and a relational database.
    """
    def __init__(self, db_session: Session = None):
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        self.db = db_session

    def set_db(self, db: Session):
        """Helper to inject the session per request if needed"""
        self.db = db

    def save_chain(self, chain: List[Block]) -> bool:
        if not self.db:
            print("⚠️ SQL Repository error: No DB session provided")
            return False
            
        try:
            for block in chain:
                # Check if block exists by index
                db_block = self.db.query(BlockModel).filter(BlockModel.index == block.index).first()
                
                if not db_block:
                    db_block = BlockModel(
                        index=block.index,
                        timestamp=block.timestamp,
                        previous_hash=block.previous_hash,
                        nonce=block.nonce,
                        block_hash=block.hash
                    )
                    self.db.add(db_block)
                    self.db.flush() # Get the ID
                    
                    # Add transactions for this new block
                    for tx in block.transactions:
                        user_id = tx.metadata.get("user_id")
                        db_tx = TransactionModel(
                            block_id=db_block.id,
                            user_id=user_id,
                            owner_address=tx.owner,
                            document_hash=tx.document_hash,
                            metadata_json=tx.metadata,
                            timestamp=tx.timestamp,
                            signature=tx.signature
                        )
                        self.db.add(db_tx)
                else:
                    # Update existing block hash and nonce if needed (unlikely in real chain but good for sync)
                    db_block.block_hash = block.hash
                    db_block.nonce = block.nonce
                    
            self.db.commit()
            return True
        except Exception as e:
            print(f"❌ Error saving chain to SQL: {str(e)}")
            self.db.rollback()
            return False

    def load_chain(self) -> List[Block]:
        if not self.db:
            return []
            
        try:
            db_blocks = self.db.query(BlockModel).order_by(BlockModel.index).all()
            chain = []
            
            for db_b in db_blocks:
                txs = []
                for t in db_b.transactions:
                    tx = Transaction(
                        owner=t.owner_address,
                        document_hash=t.document_hash,
                        metadata=t.metadata_json,
                        signature=t.signature
                    )
                    tx.timestamp = t.timestamp # Restore original timestamp
                    txs.append(tx)
                    
                block = Block(
                    index=db_b.index,
                    transactions=txs,
                    previous_hash=db_b.previous_hash,
                    timestamp=db_b.timestamp,
                    nonce=db_b.nonce,
                    hash=db_b.block_hash
                )
                chain.append(block)
            return chain
        except Exception as e:
            print(f"❌ Error loading chain from SQL: {str(e)}")
            return []

    def save_node(self, node_url: str) -> bool:
        if not self.db: return False
        try:
            exists = self.db.query(NodeModel).filter(NodeModel.url == node_url).first()
            if not exists:
                node = NodeModel(url=node_url)
                self.db.add(node)
                self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def load_nodes(self) -> List[str]:
        if not self.db: return []
        try:
            nodes = self.db.query(NodeModel).all()
            return [n.url for n in nodes]
        except:
            return []
