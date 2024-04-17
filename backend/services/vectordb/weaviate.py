import os
from logging import getLogger
from typing import Any

import weaviate
from langchain_community.vectorstores.weaviate import Weaviate

from .utils import generate_docs_from_columns
from .vectordb import VectorDatabase

# schema class name has to start with capital letter
WEAVIATE_CLASS_NAME = "Table_column_data"
# WEAVIATE_PERSISTENT_STORAGE_PATH = "./db/weaviate_data"
WEAVIATE_PERSISTENT_STORAGE_PATH = os.path.join(".", "db", "weaviate_data")

logger = getLogger("uvicorn.app")


class WeaviateDBBase(VectorDatabase):
    class_name: str

    def __init__(self, client: Any, class_name: str = WEAVIATE_CLASS_NAME):
        super().__init__(client)

        self.class_name = class_name
        # instantiate vectorstore
        logger.debug("VectorDB log: Checking if schema class exists already. If not, create schema.")
        if not self._check_class_name_exists():
            self._create_schema()

    def save(self, all_columns: list[dict], database_name: str, data_source_id: int, **kwargs):
        docs = generate_docs_from_columns(all_columns, database_name, data_source_id)

        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=["data_source_id", "database_name", "table_name"]
        )

        # insert to vectorstore
        logger.debug("VectorDB log: Inserting documents to vectorstore")
        res = vectorstore.add_documents(docs)
        logger.debug(f"VectorDB log: Inserted {len(res)} documents to vectorstore")

    def query(self, query: str, top_k: int = 5, **kwargs):
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=["data_source_id", "database_name", "table_name"]
        )
        query_embedded = self.embeddings.embed_query(query)
        # data = vectorstore.similarity_search(query, k=top_k)
        data = vectorstore.similarity_search_by_vector(
            embedding=query_embedded,
            k=top_k
        )

        # print results
        return data

    def clear(self, **kwargs):
        self.client.schema.delete_all()

    def _create_schema(self):
        # since embedded weaviate is in experimental stage, we can not use text2vec-transformers
        # https://weaviate.io/developers/weaviate/starter-guides/which-weaviate#by-vectorizer--reranker

        # define input structure
        # weaviate_client.schema.delete_all()
        # return
        schemas = self.client.schema.get()
        for schema in schemas.get("classes", []):
            if schema.get("class") == self.class_name:
                logger.warning("Schema already exists. Skipping creation.")
                return

        logger.debug("Creating schema: %s", self.class_name)
        # for more information: https://weaviate.io/developers/weaviate/config-refs/schema
        schema = {
            "classes": [
                {
                    "class": self.class_name,
                    "description": "Table column description information",
                    "vectorizer": "none",
                    "properties": [
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "The description of the column",
                        }
                    ],
                },
            ]
        }
        self.client.schema.create(schema)

    def _check_class_name_exists(self):
        # return False
        try:
            self.client.schema.get(self.class_name)
            return True
        except weaviate.exceptions.UnexpectedStatusCodeException as e:
            if e.status_code == 404:
                return False
            raise e


class WeaviateEmbedDB(WeaviateDBBase):
    def __init__(self, class_name: str = WEAVIATE_CLASS_NAME, storage_path: str = WEAVIATE_PERSISTENT_STORAGE_PATH):
        from weaviate.embedded import EmbeddedOptions

        client = weaviate.Client(
            embedded_options=EmbeddedOptions(
                persistence_data_path=storage_path
            )
        )
        super().__init__(client, class_name)


class WeaviateServerDB(WeaviateDBBase):
    def __init__(self, server_endpoint: str, class_name: str = WEAVIATE_CLASS_NAME):
        client = weaviate.Client(
            url=server_endpoint,
        )
        super().__init__(client, class_name)
