from abc import ABC, abstractmethod
from typing import Any

from langchain_core.documents import Document

from .custom_embedding import CustomEmbedding


class VectorDatabase(ABC):
    client: Any
    embeddings: Any

    def __init__(self, client: Any, embeddings: Any = None):
        self.client = client
        # embeddings with SentenceTransformers
        self.embeddings = embeddings or CustomEmbedding()

    @abstractmethod
    def save(self, docs: list[Document], **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query(self, query: str, top_k: int = 5, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query_with_filter(self, query: str, filter, top_k: int = 5, **kwargs) -> list[tuple[Document, float]]:
        raise NotImplementedError

    @abstractmethod
    def clear(self, **kwargs):
        raise NotImplementedError
