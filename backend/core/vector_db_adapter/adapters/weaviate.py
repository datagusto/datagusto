import os
from logging import getLogger
from typing import Optional

import weaviate
from langchain_community.vectorstores.weaviate import Weaviate
from langchain_core.documents import Document

from .base import VectorDatabaseBase

# schema class name has to start with capital letter
WEAVIATE_CLASS_NAME = "Table_column_data"
# WEAVIATE_PERSISTENT_STORAGE_PATH = "./db/weaviate_data"
WEAVIATE_PERSISTENT_STORAGE_PATH = os.path.join(".", "db", "weaviate_data")
WEAVIATE_DEFAULT_ENDPOINT = "http://weaviate:8005"

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
                },
            ],
        },
    ],
}


class WeaviateDBBase(VectorDatabaseBase):
    client: weaviate.client.Client
    class_name: str
    attributes: list[str] = METADATA_ATTRIBUTES
    schema: dict

    def __init__(
        self,
        client: weaviate.client.Client,
        class_name: str = WEAVIATE_CLASS_NAME,
        attributes: Optional[list[str]] = None,
    ) -> None:
        super().__init__(client)

        self.class_name = class_name
        self.schema = SCHEMA
        self.schema["classes"][0]["class"] = class_name
        self.attributes = attributes or self.attributes
        # instantiate vectorstore
        logger.debug("VectorDB log: Checking if schema class exists already. If not, create schema.")
        if not self._check_class_name_exists():
            self._create_schema()

    def save(self, docs: list[Document], **kwargs: dict) -> None:
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=self.attributes,
        )

        # insert to vectorstore
        logger.debug("VectorDB log: Inserting documents to vectorstore")
        res = vectorstore.add_documents(docs)
        logger.debug(f"VectorDB log: Inserted {len(res)} documents to vectorstore")

    def query(
        self,
        query: str,
        user_id: Optional[int],
        shared_data_source_ids: Optional[list[int]] = None,
        filter: Optional[dict] = None,
        top_k: int = 5,
        **kwargs: dict,
    ) -> list[Document]:
        shared_data_source_ids = shared_data_source_ids or []
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=self.attributes,
        )
        filter = self._add_filter_attribute(filter, "user_id", user_id)
        where_filter = {
            "operator": "And",
            "operands": [
                {"path": [key], "operator": "Equal", "valueNumber" if isinstance(value, int) else "valueString": value}
                for key, value in filter.items()
            ],
        }
        query_embedded = self.embeddings.embed_query(query)
        # data = vectorstore.similarity_search(query, k=top_k)
        data = vectorstore.similarity_search_by_vector(embedding=query_embedded, k=top_k, where_filter=where_filter)

        # print results
        return data

    def query_with_score(
        self,
        query: str,
        user_id: Optional[int],
        shared_data_source_ids: Optional[list[int]] = None,
        filter: Optional[dict] = None,
        top_k: int = 5,
        **kwargs: dict,
    ) -> list[tuple[Document, float]]:
        shared_data_source_ids = shared_data_source_ids or []
        logger.debug("VectorDB log: Creating vectorstore instance")
        vectorstore = Weaviate(
            client=self.client,
            index_name=self.class_name,
            text_key="content",
            embedding=self.embeddings,
            attributes=self.attributes,
            by_text=False,
        )
        filter = self._add_filter_attribute(filter, "user_id", user_id)
        where_filter = {
            "operator": "And",
            "operands": [
                {"path": [key], "operator": "Equal", "valueNumber" if isinstance(value, int) else "valueString": value}
                for key, value in filter.items()
            ],
        }
        # where_filter = {"path": ["some_property"], "operator": "Equal", "valueString": "som_value"}
        data = vectorstore.similarity_search_with_score(query=query, k=top_k, where_filter=where_filter)
        # print results
        return data

    def delete_by_filter(self, filter: dict, **kwargs: dict) -> dict:
        logger.debug("VectorDB log: Deleting data of data source : " + str(filter))
        data_source_id = filter["data_source_id"]
        where_filter = {
            "path": ["data_source_id"],
            "operator": "Equal",
            "valueNumber" if isinstance(data_source_id, int) else "valueString": data_source_id,
        }
        result = self.client.batch.delete_objects(
            class_name=self.class_name,
            where=where_filter,
        )
        return result

    def clear(self, **kwargs: dict) -> None:
        self.client.schema.delete_all()

    def _create_schema(self) -> None:
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

    def _check_class_name_exists(self) -> bool:
        # return False
        try:
            self.client.schema.get(self.class_name)
            return True
        except weaviate.exceptions.UnexpectedStatusCodeException as e:
            if e.status_code == 404:
                return False
            raise e


class WeaviateEmbedDB(WeaviateDBBase):
    def __init__(
        self,
        endpoint: Optional[str] = None,
        class_name: str = WEAVIATE_CLASS_NAME,
        attributes: Optional[list[str]] = None,
        **kwargs: dict,
    ) -> None:
        endpoint = endpoint or WEAVIATE_PERSISTENT_STORAGE_PATH
        from weaviate.embedded import EmbeddedOptions

        client = weaviate.Client(embedded_options=EmbeddedOptions(persistence_data_path=endpoint))
        super().__init__(client, class_name, attributes)


class WeaviateServerDB(WeaviateDBBase):
    def __init__(
        self,
        endpoint: Optional[str] = None,
        class_name: str = WEAVIATE_CLASS_NAME,
        attributes: Optional[list[str]] = None,
        **kwargs: dict,
    ) -> None:
        # embedded weaviate's path is constant, cant not be changed
        endpoint = endpoint or WEAVIATE_DEFAULT_ENDPOINT
        client = weaviate.Client(
            url=endpoint,
        )
        super().__init__(client, class_name, attributes)
