from logging import getLogger

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

logger = getLogger("uvicorn.app")


def generate_docs_from_columns(all_columns: list[dict], database_name: str, data_source_id: int) -> list[Document]:
    # instantiate text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # generate Documents object with necessary metadata
    logger.debug("VectorDB log: Generating Documents object with necessary metadata")
    documents = [Document(
        page_content=x.get("content"),
        metadata={
            "data_source_id": data_source_id,
            "database_name": database_name,
            "table_name": x.get("table_name"),
            "column_name": x.get("column_name"),
            "column_type": x.get("column_type")
        }) for x in all_columns]
    logger.debug("VectorDB log: Splitting documents")
    docs = text_splitter.split_documents(documents)
    return docs
