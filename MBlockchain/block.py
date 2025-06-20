#Estructura y Validacion de Bloques
import time
from datetime import datetime
from typing import Any, Dict, Optional
from utils import calculate_block_hash, is_valid_hash

class Block:
    def __init__(self, index: int, data: str, previous_hash: str, timestamp: Optional[float] = None):
        """
        Initialize a new block in the blockchain.
        
        Args:
            index (int): The index of the block.
            data (str): The data contained in the block.
            previous_hash (str): The hash of the previous block.
        """
        if not isinstance(index, int) or index < 0:
            raise ValueError("Index must be a non-negative integer.")
        if not isinstance(data, str):
            raise ValueError("Data must be a non-empty string.")
        if not previous_hash or not isinstance(previous_hash, str) or len(previous_hash) != 64 and previous_hash != "0":
            raise ValueError("Previous hash must be a valid SHA-256 hash (64 characters long) or '0' for the genesis block.")
            
        self.index = index
        self.timestamp = timestamp if timestamp else time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash for the block.
        
        Returns:
            str: The SHA-256 hash of the block.
        """
        return calculate_block_hash(self.index, self.timestamp, self.data, self.previous_hash, self.nonce)
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block by finding a valid hash that meets the difficulty requirement.
        
        Args:
            difficulty (int): The difficulty level, number of leading zeros required.

        Raises:
            ValueError: If difficulty is not a non-negative integer.
            Exception: If nonce limit is exceeded (mining failure).
        """
        if not isinstance(difficulty, int) or difficulty <= 0:
            raise ValueError("Difficulty must be a non-negative integer.")

        target = '0' * difficulty
        scale = 5_000_000  # Arbitrary scale factor for difficulty adjustment
        min_nonce_limit = 10_000_000  # Minimum nonce limit to prevent excessive mining time
        max_nonce = max(min_nonce_limit, difficulty * scale )  # Arbitrary limit to prevent infinite loops

        start_time = time.time()
        
        while not self.hash.startswith(target):
            self.nonce += 1
            if self.nonce >= max_nonce:
                raise Exception(f"Mining failed: Nonce limit of {max_nonce}"
                " exceeded. Try increasing the difficulty or check the mining process.")
            self.hash = self.calculate_hash()

        elapsed_time = time.time() - start_time
        print(f"Block mined successfully!")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        
    def is_valid_hash(self, difficulty: int) -> bool:
        """
        Check if the block's hash is valid according to the difficulty level.
        
        Args:
            difficulty (int): The difficulty level, number of leading zeros required.
        
        Returns:
            bool: True if the block's hash is valid, False otherwise.
        """
        if not isinstance(difficulty, int) or difficulty <= 0:
            raise ValueError("Difficulty must be a positive integer.")
        
        expected_hash = self.calculate_hash()
        
        if self.hash != expected_hash:
            raise ValueError("Block hash does not match the calculated hash.")
        
        return self.hash.startswith('0' * difficulty)


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the block to a dictionary representation.
        
        Returns:
            Dict[str, Any]: The dictionary representation of the block.
        """
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "nonce": self.nonce,
            "data": self.data
        }

    def __str__(self) -> str:
        """
        String representation of the block.
        
        Returns:
            str: The string representation of the block.
        """
        return (f"Block(index={self.index}, "
                f"timestamp={datetime.fromtimestamp(self.timestamp).isoformat()}, "
                f"data={self.data}, "
                f"previous_hash={self.previous_hash[:10]}..., "
                f"nonce={self.nonce}, "
                f"hash={self.hash[:10]}...)")
        
    def __repr__(self) -> str:
        """
        Representation of the block for debugging.
        
        Returns:
            str: The representation of the block.
        """
        return self.__str__()
    