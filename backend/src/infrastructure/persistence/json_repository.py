import json
import os
from typing import List, Dict, Any
from src.domain.interfaces.blockchain_repository import BlockchainRepository
from src.domain.entities.block import Block
from src.domain.entities.transaction import Transaction

class JSONBlockchainRepository(BlockchainRepository):
    """
    Implementation of BlockchainRepository using local JSON files.
    """
    def __init__(self, file_path: str = "blockchain.json", nodes_path: str = "nodes.json"):
        self.file_path = file_path
        self.nodes_path = nodes_path

    def save_chain(self, chain: List[Block]) -> bool:
        data = []
        for block in chain:
            block_dict = {
                "index": block.index,
                "timestamp": block.timestamp,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash,
                "transactions": [tx.to_dict() for tx in block.transactions]
            }
            data.append(block_dict)
            
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
        return True

    def load_chain(self) -> List[Block]:
        if not os.path.exists(self.file_path):
            return []
            
        with open(self.file_path, "r") as f:
            data = json.load(f)
            
        chain = []
        for b in data:
            txs = [
                Transaction(t['owner'], t['document_hash'], t['metadata'], t.get('signature')) 
                for t in b['transactions']
            ]
            for i, tx in enumerate(txs):
                tx.timestamp = b['transactions'][i]['timestamp']
                
            block = Block(b['index'], txs, b['previous_hash'], b['timestamp'], b['nonce'], b['hash'])
            chain.append(block)
        return chain

    def save_node(self, node_url: str) -> bool:
        nodes = self.load_nodes()
        if node_url not in nodes:
            nodes.append(node_url)
            with open(self.nodes_path, "w") as f:
                json.dump(nodes, f)
        return True

    def load_nodes(self) -> List[str]:
        if not os.path.exists(self.nodes_path):
            return []
        with open(self.nodes_path, "r") as f:
            return json.load(f)
