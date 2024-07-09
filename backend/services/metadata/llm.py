from logging import getLogger

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from core.llm_adapter.factory import LlmFactory

logger = getLogger("uvicorn.app")

prompt = """
You are an AI assistant that helps people to generate
description for table columns.

Here is table name and some details about the columns in the table:
Table name: {TABLE_NAME}
Column details: {COLUMN_DETAILS}

Please generate one sentence description for the column.
"""


def generate_column_description(column_info: dict, table_name: str) -> str:
    column_data = ""
    for key, value in column_info.items():
        column_data += f"{key}: {value}\n"

    _full_prompt = prompt.format(
        TABLE_NAME=table_name,
        COLUMN_DETAILS=column_data,
    )

    factory = LlmFactory()
    llm = factory.get_llm()
    res = llm.completion(_full_prompt)
    return res


def generate_docs_from_columns(
    all_columns: list[dict],
    database_name: str,
    data_source_id: int,
    user_id: int,
) -> list[Document]:
    # instantiate text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # generate Documents object with necessary metadata
    logger.debug("VectorDB log: Generating Documents object with necessary metadata")
    documents = [
        Document(
            page_content=x.get("description"),
            metadata={
                "data_source_id": data_source_id,
                "user_id": user_id,
                "database_name": database_name,
                "table_name": x.get("table_name"),
                "column_name": x.get("column_name"),
                "column_type": x.get("column_type"),
            },
        )
        for x in all_columns
    ]
    logger.debug("VectorDB log: Splitting documents")
    docs = text_splitter.split_documents(documents)
    return docs
