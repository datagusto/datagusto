import os
from logging import getLogger
from typing import Optional

from services.vectordb.faiss import FaissDB
from services.vectordb.vectordb import VectorDatabase
from services.vectordb.weaviate import WeaviateServerDB, WeaviateEmbedDB


logger = getLogger("uvicorn.app")

storage_client: Optional[VectorDatabase] = None
storage_client_join: Optional[VectorDatabase] = None

if os.environ["VECTOR_DB_USAGE_TYPE"] in ["WEAVIATE_SERVER", "WEAVIATE_EMBEDDED"]:
    # schema class name has to start with capital letter
    WEAVIATE_CLASS_NAME_JOIN = "Joined_data"

    if os.environ["VECTOR_DB_USAGE_TYPE"] == "WEAVIATE_SERVER":
        storage_client = WeaviateServerDB(os.environ["VECTOR_DB_ENDPOINT"])
        storage_client_join = WeaviateServerDB(os.environ["VECTOR_DB_ENDPOINT"], class_name=WEAVIATE_CLASS_NAME_JOIN)

    if os.environ["VECTOR_DB_USAGE_TYPE"] == "WEAVIATE_EMBEDDED":
        storage_client = WeaviateEmbedDB()
        storage_client_join = WeaviateEmbedDB(class_name=WEAVIATE_CLASS_NAME_JOIN)

if os.environ["VECTOR_DB_USAGE_TYPE"] == "FAISS":
    JOIN_DATA_PERSISTENT_STORAGE_PATH = os.path.join(".", "data", "db", "faiss_data", "joinable_table.faiss")

    storage_client = FaissDB()
    storage_client_join = FaissDB(storage_path=JOIN_DATA_PERSISTENT_STORAGE_PATH)

if storage_client is None or storage_client_join is None:
    raise Exception("VECTOR DB information is not configured properly. Please check VECTOR_DB_USAGE_TYPE in .env file")
