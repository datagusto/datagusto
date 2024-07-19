from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from langchain_core.documents import Document

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings

from ..custom_embedding import CustomEmbedding


class VectorDatabaseBase(ABC):
    client: Any
    embeddings: "Embeddings"

    def __init__(self, client: Any, embeddings: Optional["Embeddings"] = None) -> None:  # noqa: ANN401
        self.client = client
        # embeddings with SentenceTransformers
        self.embeddings = embeddings or CustomEmbedding()

    @abstractmethod
    def save(self, docs: list[Document], **kwargs: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(
        self,
        query: str,
        user_id: Optional[int],
        shared_data_source_ids: Optional[list[int]] = None,
        top_k: int = 5,
        **kwargs: dict,
    ) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def query_with_score(
        self,
        query: str,
        user_id: int,
        shared_data_source_ids: Optional[list[int]] = None,
        filter: Optional[dict] = None,
        top_k: int = 5,
        **kwargs: dict,
    ) -> list[tuple[Document, float]]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_filter(self, filter: dict, **kwargs: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def clear(self, **kwargs: dict) -> None:
        raise NotImplementedError

    def _add_filter_attribute(self, filter: Optional[dict], attribute: str, value: int) -> dict:
        filter = filter or {}
        filter.setdefault(attribute, value)
        return filter
