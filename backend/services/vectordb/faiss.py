import os
from logging import getLogger
from typing import Optional

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document

from .custom_embedding import CustomEmbedding
from .vectordb import VectorDatabase

# path need to be cross platform compatible (windows linux macos)
# FAISS_PERSISTENT_STORAGE_PATH = "./db/faiss_data/index.faiss"
FAISS_PERSISTENT_STORAGE_PATH = os.path.join(".", "db", "faiss_data", "index.faiss")

logger = getLogger("uvicorn.app")


class FaissDB(VectorDatabase):
    storage_path: str

    def __init__(self, storage_path: str = FAISS_PERSISTENT_STORAGE_PATH):
        client = None
        embeddings = CustomEmbedding()
        self.storage_path = storage_path
        super().__init__(client, embeddings=embeddings)

    def save(self, docs: list[Document], storage_path: Optional[str] = None, **kwargs):
        logger.debug("VectorDB log: Creating vectorstore instance")
        db = FAISS.from_documents(docs, self.embeddings)

        # insert to vectorstore
        logger.debug("VectorDB log: Inserting documents to vectorstore")
        local_db = self._load_local_vectorstore(storage_path)
        if local_db:
            db.merge_from(local_db)
        db.save_local(storage_path or self.storage_path)

    def query(self, query: str, user_id: Optional[int], filter=None,
              top_k: int = 5, storage_path: Optional[str] = None, **kwargs):
        filter = self._add_user_id_to_filter(filter, user_id)
        db = self._load_local_vectorstore(storage_path)
        if not db:
            return []
        docs = db.similarity_search(query, filter=filter, k=top_k)
        return docs

    def query_with_score(self, query: str, user_id: Optional[int], filter,
                         top_k: int = 5, storage_path: Optional[str] = None, **kwargs):
        filter = self._add_user_id_to_filter(filter, user_id)
        db = self._load_local_vectorstore(storage_path)
        if not db:
            return []
        results = db.similarity_search_with_score(query, filter=filter, k=top_k)
        return results

    def clear(self, storage_path: Optional[str] = None, **kwargs):
        db = self._load_local_vectorstore(storage_path)
        if db:
            indexes = list(db.index_to_docstore_id.values())
            if len(indexes) > 0:
                db.delete(indexes)
                db.save_local(storage_path or self.storage_path)

    def _load_local_vectorstore(self, storage_path: Optional[str] = None):
        path = storage_path or self.storage_path
        if os.path.exists(path):
            return FAISS.load_local(
                folder_path=self.storage_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
        return None
