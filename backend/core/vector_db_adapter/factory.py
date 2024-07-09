import os
from logging import getLogger

from .adapters.base import VectorDatabaseBase
from .adapters.faiss import FaissDB
from .adapters.weaviate import WeaviateEmbedDB, WeaviateServerDB

logger = getLogger("uvicorn.app")

ADAPTERS = {
    'WEAVIATE_SERVER': WeaviateServerDB,
    "WEAVIATE_EMBEDDED": WeaviateEmbedDB,
    "FAISS": FaissDB,
}


class VectorDatabaseFactory:
    join_data_class_name = "Joined_data"

    def __init__(self):
        adapter_name = os.environ["VECTOR_DB_USAGE_TYPE"]
        if adapter_name not in ADAPTERS:
            raise ValueError(f"Vector database is not configured properly. Please check VECTOR_DB_USAGE_TYPE in .env file.")
        self.adapter_name = adapter_name

    def get_vector_database(self) -> "VectorDatabaseBase":
        logger.debug(f"Creating {self.adapter_name} vector database connection.")
        endpoint = os.getenv("VECTOR_DB_ENDPOINT", None)
        adapter = ADAPTERS[self.adapter_name]
        return adapter(
            endpoint=endpoint
        )

    def get_vector_database_join(self) -> "VectorDatabaseBase":
        logger.debug(f"Creating {self.adapter_name} vector database join connection.")
        endpoint = os.getenv("VECTOR_DB_ENDPOINT", None)
        adapter = ADAPTERS[self.adapter_name]
        return adapter(
            endpoint=endpoint,
            class_name=self.join_data_class_name
        )
