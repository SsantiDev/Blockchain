from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.block import Block

class BlockchainRepository(ABC):
    """
    Interface for persisting and retrieving the blockchain state.
    """
    @abstractmethod
    def save_chain(self, chain: List[Block]) -> bool:
        pass

    @abstractmethod
    def load_chain(self) -> List[Block]:
        pass

    @abstractmethod
    def save_node(self, node_url: str) -> bool:
        pass

    @abstractmethod
    def load_nodes(self) -> List[str]:
        pass
