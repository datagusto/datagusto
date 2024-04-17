from logging import getLogger
import base64

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import pandas as pd

import crud
import models
import schemas
from database import SessionLocal, engine
from services.connections import get_connection
from services.generative_llm import generate_column_description
from services.metadata import get_metadata, save_metadata
from services.vectordb.load import storage_client
from services.joinable_table.offline import indexing
from services.joinable_table.online import join_data
from adapters.mysql import MySQLConnection

logger = getLogger("uvicorn.app")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

    # TODO: create getter for connection
    connection = None
    if data_source.type == schemas.DataSourceType.MySQL:
        logger.debug("Creating MySQL connection: data_source_id=%s", data_source_id)
        connection = MySQLConnection(config=data_source.connection)
    
    columns = [c.column_name for c in crud.get_columns_in_table(db, data_source_id, table_name)]
    sample_data = connection.select_table(table_name, limit=5)
    df = pd.DataFrame(sample_data, columns=columns)

    binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
    for column in binary_columns:
        df[column] = df[column].apply(encode_binary)
    response = {}
    response["data"] = df.to_json(orient="records")
    return response


@app.post("/data_sources/", response_model=schemas.DataSource)
def create_data_source(ds: schemas.DataSourceCreate, db: Session = Depends(get_db)):
    # initialize connection based on the data source type
    logger.info("Creating data source, and checking db connection info correct.: %s", ds.name)
    connection = get_connection(ds.type, ds.connection)

    # test connection with the credentials
    logger.info("Testing connection with the credentials. %s", ds.name)
    if not connection.test_connection():
        logger.exception("Invalid connection data. %s", ds.name)
        raise HTTPException(status_code=400, detail="Invalid connection data")

    logger.info("Creating data source in the database. %s", ds.name)
    data_source = crud.create_data_source(db=db, data_source=ds)
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
    storage_client.save(all_columns, database_name, data_source_id)

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

        # TODO: create getter for connection
        connection = None
        if data_source.type == schemas.DataSourceType.MySQL:
            logger.debug("Creating MySQL connection: data_source_id=%s", data_source_id)
            connection = MySQLConnection(config=data_source.connection)
        
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
    logger.info("Clearing Database")
    crud.clear_database_column_information(db)
    return {"message": "VectorDB cleared."}


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

    response_body = {}
    response_body["data"] = merged_df.to_json(orient="records")
    response_body["joinable_info"] = joinable_info
    
    return response_body
