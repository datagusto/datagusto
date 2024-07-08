from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.orm import Session

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from core.data_source_adapter.factory import DataSourceFactory
from core.vector_db_adapter.factory import VectorDatabaseFactory
from database.crud import data_source as data_source_crud
from database.crud import metadata as metadata_crud
from .sub import generate_text_from_data, flatten_concatenation

logger = getLogger("uvicorn.app")


def indexing(data_source_id: int, user_id: int, db: Session):
    # TODO: this need to be triggered when new data source is added automatically
    # load tokenizer
    # model_path = "./models/model_ver1.0"
    # model, tokenizer = load_model(model_path)

    # get data from target data source
    data_source = data_source_crud.get_data_source(db, data_source_id=data_source_id, user_id=user_id)
    if not data_source:
        logger.warning("data_source_id: %s not found", data_source_id)
        return HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")
    
    # create connection to data source
    factory = DataSourceFactory(
        adapter_name=data_source.type,
        name=data_source.name,
        description=data_source.description,
        connection=data_source.connection
    )
    connection = factory.get_data_source()

    # create index
    database_information_list = metadata_crud.get_database_information(db, data_source_id, user_id)
    repository_texts = []
    docs = []
    for database_information in database_information_list:
        for table_information in database_information.table_information:
            for column in table_information.table_info["columns"]:
                logger.info("data_source_id: %s, table_name: %s, column_name: %s, column_type: %s",
                            data_source_id, table_information.table_name, column["column_name"], column["column_type"])
                # skip unsupported column types
                # TODO: check with the white list of supported column types instead of black list
                if column["column_type"].startswith(("timestamp", "geometry", "year", "decimal", "enum", "set", "datetime", "blob")):
                    continue
                # select column data
                data = connection.select_column(table_information.table_name, column["column_name"], limit=1000)
                data = flatten_concatenation(data)
                logger.info("data: %s", data[:5])
                # generate text
                text = generate_text_from_data(table_information.table_name, column["column_name"], data)
                logger.info("text: %s", text[:50])
                repository_texts.append(text)

                docs.append(Document(
                    page_content=text,
                    metadata={
                        "data_source_id": data_source_id,
                        "user_id": user_id,
                        "database_name": data_source.name,
                        "table_name": table_information.table_name,
                        "column_name": column["column_name"],
                        "column_type": column["column_type"]
                    })
                )

    # save index
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)
    factory = VectorDatabaseFactory()
    vector_db_join_client = factory.get_vector_database_join()
    vector_db_join_client.save(docs)
    
    # tokenize texts
    # inputs = tokenizer(repository_texts, return_tensors="pt", padding=True, truncation=True, max_length=128)
    # outputs = model(**inputs)
    # last_hidden_states = outputs.last_hidden_state
    # cls_token_vector = last_hidden_states[:, 0, :].detach().cpu().numpy()

    # # create faiss index
    # d = cls_token_vector.shape[1]
    # index = faiss.IndexFlatL2(d)
    
    # # persist faiss index
    # faiss.write_index(index, "./db/faiss/{data_source_id}.index")