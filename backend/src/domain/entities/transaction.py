from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class Transaction:
    """
    Pure Domain Entity representing a Notary Transaction.
    """
    owner: str
    document_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    signature: Optional[str] = None

    def to_dict(self, include_signature: bool = True) -> Dict[str, Any]:
        data = {
            "owner": self.owner,
            "document_hash": self.document_hash,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
        if include_signature:
            data["signature"] = self.signature
        return data

    def __post_init__(self):
        if not self.owner or not self.document_hash:
            raise ValueError("Owner and Document Hash are mandatory for a Transaction")
