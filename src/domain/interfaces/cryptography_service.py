from abc import ABC, abstractmethod
from typing import Dict, Any

class CryptographyService(ABC):
    """
    Interface for cryptographic operations: hashing, signing, and verification.
    """
    @abstractmethod
    def calculate_hash(self, data: Any) -> str:
        pass

    @abstractmethod
    def sign_data(self, data: str, private_key: Any) -> str:
        pass

    @abstractmethod
    def verify_signature(self, public_key: str, signature: str, data: str) -> bool:
        pass

    @abstractmethod
    def generate_key_pair(self) -> Dict[str, Any]:
        pass
