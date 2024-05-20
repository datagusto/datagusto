import os
from logging import getLogger
from typing import Any

import weaviate
from langchain_community.vectorstores.weaviate import Weaviate
from langchain_core.documents import Document

from .vectordb import VectorDatabase

# schema class name has to start with capital letter
WEAVIATE_CLASS_NAME = "Table_column_data"
# WEAVIATE_PERSISTENT_STORAGE_PATH = "./db/weaviate_data"
WEAVIATE_PERSISTENT_STORAGE_PATH = os.path.join(".", "db", "weaviate_data")

METADATA_ATTRIBUTES = ["data_source_id", "database_name", "table_name", "column_name", "column_type"]

logger = getLogger("uvicorn.app")

SCHEMA = {
    "classes": [
        {
            "class": "Class_name",
            "description": "Description",
            "vectorizer": "none",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The content of the document",
                }
            ],
        },
    ]
}


class WeaviateDBBase(VectorDatabase):
    class_name: str
    attributes: list[str] = METADATA_ATTRIBUTES
    schema: dict

    def __init__(self, client: Any, class_name: str = WEAVIATE_CLASS_NAME, attributes: list[str] = None):
        super().__init__(client)

        self.class_name = class_name
        self.schema = SCHEMA
        self.schema["classes"][0]["class"] = class_name
        self.attributes = attributes or self.attributes
        # instantiate vectorstore
        logger.debug("VectorDB log: Checking if schema class exists already. If not, create schema.")
        if not self._check_class_name_exists():
            self._create_schema()

    def save(self, docs: list[Document], **kwargs):
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=self.attributes
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
            attributes=self.attributes
        )
        query_embedded = self.embeddings.embed_query(query)
        # data = vectorstore.similarity_search(query, k=top_k)
        data = vectorstore.similarity_search_by_vector(
            embedding=query_embedded,
            k=top_k
        )

        # print results
        return data

    def query_with_filter(self, query: str, filter, top_k: int = 5, **kwargs):
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=self.attributes,
            by_text=False
        )
        where_filter = {
            "operator": "And",
            "operands": []
        }
        for key, value in filter.items():
            where_filter["operands"].append({
                "path": [key],
                "operator": "Equal",
                "valueString": value
            })
        # where_filter = {"path": ["some_property"], "operator": "Equal", "valueString": "som_value"}
        data = vectorstore.similarity_search_with_score(
            query=query,
            k=top_k,
            where_filter=where_filter
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
        self.client.schema.create(self.schema)

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
    def __init__(self, class_name: str = WEAVIATE_CLASS_NAME, storage_path: str = WEAVIATE_PERSISTENT_STORAGE_PATH, attributes: list[str] = None):
        from weaviate.embedded import EmbeddedOptions

        client = weaviate.Client(
            embedded_options=EmbeddedOptions(
                persistence_data_path=storage_path
            )
        )
        super().__init__(client, class_name, attributes)


class WeaviateServerDB(WeaviateDBBase):
    def __init__(self, server_endpoint: str, class_name: str = WEAVIATE_CLASS_NAME, attributes: list[str] = None):
        client = weaviate.Client(
            url=server_endpoint,
        )
        super().__init__(client, class_name, attributes)
