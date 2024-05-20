import os
from logging import getLogger
import base64

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from services.vectordb.utils import generate_docs_from_columns

load_dotenv(dotenv_path=".env")

from database import crud
from database import models
import pandas as pd

import schemas
from database.database import SessionLocal, engine
from services.generative_llm import generate_column_description
from services.metadata import get_metadata, save_metadata
from services.vectordb.load import storage_client, storage_client_join
from services.joinable_table.offline import indexing
from services.joinable_table.online import join_data
from adapters.connections import get_connection

logger = getLogger("uvicorn.app")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "*",   # Allow any origin for now
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def encode_binary(value):
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    else:
        return value


@app.get("/data_sources/", response_model=list[schemas.DataSource])
def get_data_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data_sources = crud.get_data_sources(db, skip=skip, limit=limit)
    return data_sources


@app.get("/data_sources/{data_source_id}", response_model=schemas.DataSource)
def get_user(data_source_id: int, db: Session = Depends(get_db)):
    data_source = crud.get_data_source(db, data_source_id=data_source_id)
    if not data_source:
        raise HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")
    return data_source


@app.get("/data_sources/{data_source_id}/table_name/{table_name}")
def get_columns_in_table(data_source_id: int, table_name: str, db: Session = Depends(get_db)):
    data_source = crud.get_data_source(db, data_source_id=data_source_id)

    connection = get_connection(data_source)
    columns = [c.column_name for c in crud.get_columns_in_table(db, data_source_id, table_name)]
    sample_data = connection.select_table(table_name, limit=5)
    df = pd.DataFrame(sample_data, columns=columns)

    binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
    for column in binary_columns:
        df[column] = df[column].apply(encode_binary)
    response = {"data": df.to_json(orient="records")}
    return response


@app.post("/data_sources/", response_model=schemas.DataSource)
def create_data_source(data_source: schemas.DataSourceCreate, db: Session = Depends(get_db)):
    # initialize connection based on the data source type
    logger.info("Creating data source, and checking db connection info correct.: %s", data_source.name)
    connection = get_connection(data_source)

    # test connection with the credentials
    logger.info("Testing connection with the credentials. %s", data_source.name)
    if not connection.test_connection():
        logger.exception("Invalid connection data. %s", data_source.name)
        raise HTTPException(status_code=400, detail="Invalid connection data")

    logger.info("Creating data source in the database. %s", data_source.name)
    data_source = crud.create_data_source(db=db, data_source=data_source)
    return data_source


@app.post("/metadata/")
def get_metadata_data_sources(model: schemas.DataSourceGetMetadata, db: Session = Depends(get_db)):
    data_source_id = model.data_source_id

    # get metadata to db
    logger.info("Getting metadata for data source: %s", data_source_id)
    tables_columns, database_name = get_metadata(model.data_source_id, db)

    # generate column description using LLM
    logger.info("Generating column description using LLM")
    for table_name, columns in tables_columns.items():
        logger.info(f"Generating column description for table: {table_name=}")
        for column in columns:
            logger.info(f"Generating column description for column: {table_name=}, {column=}")
            column["description"] = generate_column_description(column, table_name)

    # save metadata to db
    logger.info("Saving metadata to the database")
    save_metadata(data_source_id, database_name, tables_columns, db)

    # save embedded metadata to vectordb
    logger.info("Saving metadata to VectorDB")
    all_columns = []
    for table_name, columns in tables_columns.items():
        all_columns.extend([
            {
                "table_name": table_name,
                "content": column["description"]
            } for column in columns])
    docs = generate_docs_from_columns(all_columns, database_name, data_source_id)
    storage_client.save(docs)

    # create joinable table index
    logger.info("Create joinable data index: %s", data_source_id)
    indexing(data_source_id, db)

    return {"message": "Getting metadata completed."}


@app.get("/metadata/query/")
def query_data_sources(query: str, db: Session = Depends(get_db)):
    result = storage_client.query(query, top_k=10)
    logger.info(f"Search result for {query} is : {result}")

    response_with_duplicated_tables = [
        {
            "data_source_id": r.metadata.get("data_source_id"),
            "data_source_name": crud.get_data_source(db, r.metadata.get("data_source_id")).name,
            "database_name": r.metadata.get("database_name"),
            "table_name": r.metadata.get("table_name"),
            "column_description": [r.page_content]
        } for r in result]

    # combine the response with the same table name
    response = []
    for r in response_with_duplicated_tables:
        exists = False
        for r_ in response:
            if r_["table_name"] == r["table_name"]:
                r_.get("column_description").extend(r["column_description"])
                exists = True
                break
        if exists is False:
            response.append(r)

    # get sample data for each table
    for r in response:
        data_source_id = r["data_source_id"]
        table_name = r["table_name"]
        data_source = crud.get_data_source(db, data_source_id=data_source_id)

        connection = get_connection(data_source)
        columns = [c.column_name for c in crud.get_columns_in_table(db, data_source_id, table_name)]
        sample_data = connection.select_table(table_name, limit=5)
        df = pd.DataFrame(sample_data, columns=columns)

        binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
        for column in binary_columns:
            df[column] = df[column].apply(encode_binary)

        r["sample_data"] = df.to_json(orient="records")

        logger.info(f"r: {r}")

    return response


@app.delete("/metadata/")
def delete_vector_db(db: Session = Depends(get_db)):
    logger.info("Clearing VectorDB")
    storage_client.clear()
    storage_client_join.clear()
    logger.info("Clearing Database")
    crud.clear_database_column_information(db)
    return {"message": "Database and VectorDB are cleared."}


@app.post("/joinable_table/indexing/")
def post_joinable_table_indexing(body: schemas.JoinableTableIndexingCreate, db: Session = Depends(get_db)):
    data_source_id = body.data_source_id
    logger.info("Indexing data source: %s", data_source_id)

    indexing(data_source_id, db)

    return {"message": "Joinable data index created."}


@app.post("/joinable_table/join_data/")
def post_joinable_table_join_data(body: schemas.JoinableTableJoinData, db: Session = Depends(get_db)):
    logger.info("Joining data")
    data_source_id = body.data_source_id
    table_name = body.table_name
    merged_df, joinable_info = join_data(data_source_id, table_name, db)

    response_body = {"data": merged_df.to_json(orient="records"), "joinable_info": joinable_info}

    return response_body


@app.exception_handler(Exception)
def exception_handler(request, exc):
    logger.exception(exc)
    return {
        "message": "Internal Server Error",
        "detail": str(exc)
    }, 200
