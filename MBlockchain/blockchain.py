#Logica de la Cadena de Bloques
from typing import List, Dict, Any
from block import Block

class Blockchain:
    def __init__(self, difficulty: int = 2):
        """
        Initialize the blockchain with a genesis block.
        
        Args:
            difficulty (int): The difficulty level for mining blocks, default is 2.
        """
        if not isinstance(difficulty, int) or difficulty <= 0:
            raise ValueError("Difficulty must be a positive integer.")
        
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis_block()
        
    def create_genesis_block(self, data: str = "Genesis Block") -> None:
        """
        The genesis block is the first block in the blockchain.
        It has no previous block, so its previous_hash is set to "0".
        
        Args:
            data (str): The data to be included in the genesis block.
        """
        genesis_block = Block(0, data, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        
    def get_latest_block(self) -> Block:
        """
        Get the latest block in the blockchain.
        
        Returns:
            Block: The latest block in the chain.
        """
        if not self.chain:
            raise ValueError("Blockchain is empty. No blocks available.")
        return self.chain[-1]
    
    def is_valid_chain(self) -> bool:
        """
        Validate the entire blockchain.
        
        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        # Check if the chain is empty
        if not self.chain:
            print("Blockchain is empty. Cannot validate an empty chain.")
            return False
        
        # Check the genesis block
        genesis_block = self.chain[0]
        if genesis_block.index != 0 or genesis_block.previous_hash != "0":
            print("Genesis block is invalid.")
            return False
        
        # Validate each block in the chain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if the current block's hash meets the difficulty requirement
            if not current_block.is_valid_hash(self.difficulty):
                print(f"Block {current_block.index} does not meet the difficulty requirement.")
                return False
            
            # Validate block hash integrity
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {current_block.index}. Expected {current_block.calculate_hash()}, got {current_block.hash}")
                return False
            
            # check if the previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {current_block.index}.")
                return False
            
        return True
    
    
    def add_block(self, data: str) -> Block:
        """
        Add a new block to the blockchain.
        
        Args:
            data (str): The data to be included in the new block.
        
        Returns:
            Block: The newly created and mined block.
            
        Raises:
            ValueError: If the data is not a string or if the block cannot be mined.
        """
        if not isinstance(data, str) or not data:
            raise ValueError("Data must be a non-empty string.")
        
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_block = Block(new_index, data, previous_block.hash)
        
        # Mine the new block
        try:
            new_block.mine_block(self.difficulty)
            self.chain.append(new_block)
            return new_block
        except Exception as e:
            print(f"Error mining block: {e}")
            raise
        
    def get_chain_info(self) -> Dict[str, Any]:
        """
        Get information about the blockchain.
        
        Returns:
            Dict[str, Any]: summary of the blockchain including total blocks, difficulty, latest block hash, and validity.
        """
        return {
            "total_blocks": len(self.chain),
            "difficulty": self.difficulty,
            "lastest_block_hash": self.get_latest_block().hash,
            "is_valid": self.is_valid_chain(),
        }
        
    def print_chain(self) -> None:
        """
        Print the entire blockchain in a readable format.
        """
        print("=" * 40)
        print("📦 Blockchain Contents 📦")
        print("=" * 40)
        
        for block in self.chain:
            print(block) # This will call the __str__ method of the Block class
            print("-" * 40)
            
        print(f"Total blocks in the chain: {len(self.chain)}")
        print(f"Difficulty level: {self.difficulty}")
        print(f"Is the blockchain valid? {self.is_valid_chain()}")
        print("=" * 40)
        
        
    