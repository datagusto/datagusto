from logging import getLogger
from transformers import MPNetModel, MPNetTokenizer
import torch
import os
import numpy as np

from langchain_community.vectorstores.faiss import FAISS


from services.vectordb.faiss import FaissDB

logger = getLogger("uvicorn.app")

FAISS_PERSISTENT_STORAGE_PATH = os.path.join(".", "db", "faiss_data", "joinable_table.faiss")


class JoinableTableIndexDB(FaissDB):
    def save(self, docs, **kwargs):
        db = FAISS.from_documents(docs, self.embeddings)
        # insert to vectorstore
        logger.debug("VectorDB log: Inserting documents to vectorstore")
        local_db = self._load_local_vectorstore()
        if local_db:
            db.merge_from(local_db)
        db.save_local(self.storage_path)

    def query_with_filter(self, query, filter, top_k=5, **kwargs):
        db = self._load_local_vectorstore()
        if not db:
            return []
        results = db.similarity_search_with_score(query, filter=filter, k=top_k)
        return results


faiss_client = JoinableTableIndexDB(storage_path=FAISS_PERSISTENT_STORAGE_PATH)


def flatten_concatenation(matrix):
     flat_list = []
     for row in matrix:
         flat_list += row
     return flat_list


def load_model(model_path):
    model = MPNetModel.from_pretrained(model_path)
    tokenizer = MPNetTokenizer.from_pretrained(model_path)
    
    return model, tokenizer


def generate_text_from_data(table_name, column_name, values):
    # TODO: Implement the logic to switch between different types of columns
    values = [str(value) for value in values]
    value_set = set(values)
    max_length = max(len(value) for value in values)
    min_length = min(len(value) for value in values)
    mean_length = np.mean([len(value) for value in values])

    text = f"{table_name}.{column_name} contains {len(values)} values (max: {max_length}, min: {min_length}, mean: {round(mean_length, 1)}): {', '.join(value_set)}."
    return text


def generate_faiss_docs():
    documents = [Document(
        page_content=x.get("content"),
        metadata={
            "data_source_id": data_source_id,
            "database_name": database_name,
            "table_name": x.get("table_name"),
        }) for x in all_columns]