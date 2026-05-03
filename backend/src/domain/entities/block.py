from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from .transaction import Transaction

@dataclass
class Block:
    """
    Pure Domain Entity representing a Block in the chain.
    """
    index: int
    transactions: List[Transaction]
    previous_hash: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    nonce: int = 0
    hash: Optional[str] = None

    def __post_init__(self):
        if self.index < 0:
            raise ValueError("Block index cannot be negative")

    def to_dict(self, include_signature: bool = True) -> Dict[str, Any]:
        """
        Convert block to dict for hashing. 
        Note: The 'hash' itself is excluded from the dict to ensure consistency.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "transactions": [tx.to_dict(include_signature) for tx in self.transactions]
        }
