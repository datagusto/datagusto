from abc import ABC, abstractmethod
from typing import Any

from .custom_embedding import CustomEmbedding


class VectorDatabase(ABC):
    client: Any
    embeddings: Any

    def __init__(self, client: Any, embeddings: Any = None):
        self.client = client
        # embeddings with SentenceTransformers
        self.embeddings = embeddings or CustomEmbedding()

    @abstractmethod
    def save(self, all_columns: list[dict], database_name: str, data_source_id: int, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query(self, query: str, top_k: int = 5, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def clear(self, **kwargs):
        raise NotImplementedError
