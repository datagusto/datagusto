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
    def query(self, query: str, user_id: Optional[int], shared_data_source_ids: Optional[list[int]] = None, top_k: int = 5, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query_with_score(self, query: str, user_id: int, shared_data_source_ids: Optional[list[int]] = None, filter: Optional[dict] = None, top_k: int = 5, **kwargs) -> list[tuple[Document, float]]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_by_filter(self, filter: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def clear(self, **kwargs):
        raise NotImplementedError

    def _add_filter_attribute(self, filter: Optional[dict], attribute: str, value: Any):
        filter = filter or {}
        filter.setdefault(attribute, value)
        return filter
