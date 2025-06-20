#Funciones Auxiliares (Hashes, timestamp, etc.)
import hashlib
import json
from typing import Any, Dict

def calculate_hash(data: Any) -> str:
    """
    Calculate the SHA-256 hash of the given data.
    
    Args:
        data (Any): The data to hash, can be a dictionary or any other type.
    
    Returns:
        str: The SHA-256 hash of the data.
    """
    try:
        if isinstance(data, dict):
            data_string = json.dumps(data, sort_keys=True)
        else:
            data_string = json.dumps(data, sort_keys=True) if not isinstance(data, str) else data
    except (TypeError, ValueError):
        # Si no es serializable, convierte a string directamente
        data_string = str(data)
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def calculate_block_hash(index: int, timestamp: float, data: str, previous_hash: str, nonce: int = 0) -> str:
    """
    Calculate the hash for a block in the blockchain.
    
    Args:
        index (int): The index of the block.
        timestamp (float): The timestamp of the block.
        data (str): The data contained in the block.
        previous_hash (str): The hash of the previous block.
        nonce (int, optional): The nonce used for mining. Defaults to 0.
    
    Returns:
        str: The SHA-256 hash of the block.
    """
    block_data = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "nonce": nonce
    }
    block_string = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

def is_valid_hash(hash_value: str, difficulty: int) -> bool:
    """
    Check if the hash meets the difficulty requirement.
    
    Args:
        hash_value (str): The hash to check.
        difficulty (int): The difficulty level, number of leading zeros required.
    
    Returns:
        bool: True if the hash meets the difficulty, False otherwise.
    """
    return hash_value.startswith('0' * difficulty)
    


    
