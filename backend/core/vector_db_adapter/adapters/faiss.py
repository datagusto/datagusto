import os
from logging import getLogger
from typing import Optional

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document

from ..custom_embedding import CustomEmbedding
from .base import VectorDatabaseBase

FAISS_PERSISTENT_STORAGE_DIRECTORY = os.path.join(".", "data", "db", "faiss_data")
FAISS_PERSISTENT_STORAGE_PATH = os.path.join(FAISS_PERSISTENT_STORAGE_DIRECTORY, "index.faiss")

logger = getLogger("uvicorn.app")


class FaissDB(VectorDatabaseBase):
    storage_path: str

    def __init__(self, endpoint: Optional[str] = None, **kwargs: dict) -> None:
        # FAISS's path is constant, cant not be changed
        endpoint = FAISS_PERSISTENT_STORAGE_PATH
        if "class_name" in kwargs:
            endpoint = os.path.join(FAISS_PERSISTENT_STORAGE_DIRECTORY, f"{kwargs['class_name']}.faiss")
        client = None
        embeddings = CustomEmbedding()
        self.storage_path = endpoint
        super().__init__(client, embeddings=embeddings)

    def save(self, docs: list[Document], storage_path: Optional[str] = None, **kwargs: dict) -> None:
        logger.debug("VectorDB log: Creating vectorstore instance")
        db = FAISS.from_documents(docs, self.embeddings)

        # insert to vectorstore
        logger.debug("VectorDB log: Inserting documents to vectorstore")
        local_db = self._load_local_vectorstore(storage_path)
        if local_db:
            db.merge_from(local_db)
        db.save_local(storage_path or self.storage_path)

    def query(
        self,
        query: str,
        user_id: int,
        shared_data_source_ids: Optional[list[int]] = None,
        filter: Optional[dict] = None,
        top_k: int = 5,
        storage_path: Optional[str] = None,
        **kwargs: dict,
    ) -> list[Document]:
        shared_data_source_ids = shared_data_source_ids or []
        db = self._load_local_vectorstore(storage_path)
        if not db:
            return []

        # search through owned data sources
        _filter = self._add_filter_attribute(filter, "user_id", user_id)
        docs = db.similarity_search(query, filter=_filter, k=top_k)

        # search through shared data sources
        for data_source_id in shared_data_source_ids:
            _filter = self._add_filter_attribute(filter, "data_source_id", data_source_id)
            docs.extend(db.similarity_search(query, filter=_filter, k=top_k))
        return docs

    def query_with_score(
        self,
        query: str,
        user_id: int,
        shared_data_source_ids: Optional[list[int]] = None,
        filter: Optional[dict] = None,
        top_k: int = 5,
        storage_path: Optional[str] = None,
        **kwargs: dict,
    ) -> list[tuple[Document, float]]:
        shared_data_source_ids = shared_data_source_ids or []
        db = self._load_local_vectorstore(storage_path)
        if not db:
            return []
        # search through owned data sources
        _filter = self._add_filter_attribute(filter, "user_id", user_id)
        results = db.similarity_search_with_score(query, filter=_filter, k=top_k)

        # search through shared data sources
        for data_source_id in shared_data_source_ids:
            _filter = self._add_filter_attribute(filter, "data_source_id", data_source_id)
            results.extend(db.similarity_search_with_score(query, filter=_filter, k=top_k))
        return results

    def delete_by_filter(self, filter: dict, storage_path: Optional[str] = None, **kwargs: dict) -> bool:
        db = self._load_local_vectorstore(storage_path)
        if not db:
            return False

        doc_id_list = []
        for doc_id, doc in db.docstore._dict.items():
            is_match = all(doc.metadata.get(key) == value for key, value in filter.items())
            if is_match:
                doc_id_list.append(doc_id)

        if len(doc_id_list) > 0:
            db.delete(doc_id_list)
            db.save_local(storage_path or self.storage_path)
            return True

        return False

    def clear(self, storage_path: Optional[str] = None, **kwargs: dict) -> None:
        db = self._load_local_vectorstore(storage_path)
        if db:
            indexes = list(db.index_to_docstore_id.values())
            if len(indexes) > 0:
                db.delete(indexes)
                db.save_local(storage_path or self.storage_path)

    def _load_local_vectorstore(self, storage_path: Optional[str] = None) -> Optional[FAISS]:
        path = storage_path or self.storage_path
        if os.path.exists(path):
            return FAISS.load_local(
                folder_path=self.storage_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True,
            )
        return None
