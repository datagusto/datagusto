from logging import getLogger
from typing import Optional

from services.vectordb.faiss import FaissDB
from services.vectordb.vectordb import VectorDatabase
from services.vectordb.weaviate import WeaviateServerDB, WeaviateEmbedDB
from settings import get_settings

logger = getLogger("uvicorn.app")

storage_client: Optional[VectorDatabase] = None

if get_settings().VECTOR_DB_USAGE_TYPE == "WEAVIATE_SERVER":
    storage_client = WeaviateServerDB(get_settings().VECTOR_DB_ENDPOINT)

if get_settings().VECTOR_DB_USAGE_TYPE == "WEAVIATE_EMBEDDED":
    storage_client = WeaviateEmbedDB()

if get_settings().VECTOR_DB_USAGE_TYPE == "FAISS":
    storage_client = FaissDB()

if storage_client is None:
    raise Exception("VECTOR DB information is not configured properly. Please check VECTOR_DB_USAGE_TYPE in .env file")
