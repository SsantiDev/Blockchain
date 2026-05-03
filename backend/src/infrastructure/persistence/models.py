from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    wallet_address = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    
    transactions = relationship("TransactionModel", back_populates="user")

class BlockModel(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, unique=True)
    timestamp = Column(Float)
    previous_hash = Column(String)
    nonce = Column(Integer)
    block_hash = Column(String, unique=True)
    
    transactions = relationship("TransactionModel", back_populates="block")

class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    owner_address = Column(String)
    document_hash = Column(String)
    metadata_json = Column(JSON)
    timestamp = Column(Float)
    signature = Column(String, nullable=True)
    
    block = relationship("BlockModel", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

class NodeModel(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
