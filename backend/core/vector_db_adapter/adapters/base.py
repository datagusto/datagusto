from abc import ABC, abstractmethod
from typing import Any, Optional

from langchain_core.documents import Document

from ..custom_embedding import CustomEmbedding
from ...abac.check import get_accessible_resource_ids


class VectorDatabaseBase(ABC):
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
    def query(self, query: str, user_id: Optional[int], top_k: int = 5, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query_with_score(self, query: str, user_id: int, filter, top_k: int = 5, **kwargs) -> list[tuple[Document, float]]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_by_filter(self, filter: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def clear(self, **kwargs):
        raise NotImplementedError

    def _add_user_id_to_filter(self, filter: Optional[dict], user_id: Optional[int]):
        if user_id:
            filter = filter or {}
            filter.setdefault("user_id", user_id)
        return filter
