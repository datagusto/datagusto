from logging import getLogger
import base64
from io import StringIO
import json

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

load_dotenv(dotenv_path=".env")

from database import crud
from database import models
import pandas as pd

import schemas
from core.auth import authenticate_user, generate_bearer_token, oauth2_scheme, verify_access_token
from services.vectordb.utils import generate_docs_from_columns
from database.database import SessionLocal, engine
from services.generative_llm import generate_column_description
from services.metadata import get_metadata, save_metadata
from services.vectordb.load import storage_client, storage_client_join
from services.joinable_table.offline import indexing
from services.joinable_table.online import join_data
from adapters.connections import get_connection
from services.data_matching.data_matching import find_schema_matching, find_data_matching

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


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    user = verify_access_token(token, db)
    return user


@app.post("/user/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    _user = crud.get_user(db, username=user.username)
    if _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = crud.create_user(db, user)
    return new_user


@app.post("/user/login", response_model=dict)
def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login.username, user_login.password)
    return generate_bearer_token(user.username)


@app.get("/user/me", response_model=schemas.UserResponse)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@app.get("/data_sources/", response_model=list[schemas.DataSource])
def get_data_sources(skip: int = 0, limit: int = 100, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    data_sources = crud.get_data_sources(db, skip=skip, limit=limit, user_id=current_user.id)
    return data_sources


@app.get("/data_sources/{data_source_id}", response_model=schemas.DataSource)
def get_data_source_by_id(data_source_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    data_source = crud.get_data_source(db, data_source_id=data_source_id, user_id=current_user.id)
    if not data_source:
        raise HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")
    return data_source


@app.get("/data_sources/{data_source_id}/table_name/{table_name}")
def get_columns_in_table(data_source_id: int, table_name: str, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    data_source = crud.get_data_source(db, data_source_id=data_source_id, user_id=current_user.id)

    connection = get_connection(data_source)
    table_information = crud.get_table(db, data_source_id, table_name, current_user.id)
    columns = [col["column_name"] for col in table_information.table_info.get("columns")]
    sample_data = connection.select_table(table_name, limit=5)
    df = pd.DataFrame(sample_data, columns=columns)

    binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
    for column in binary_columns:
        df[column] = df[column].apply(encode_binary)
    response = {"data": df.to_json(orient="records")}
    return response


@app.post("/data_sources/", response_model=schemas.DataSource)
def create_data_source(data_source: schemas.DataSourceCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # initialize connection based on the data source type
    logger.info("Creating data source, and checking db connection info correct.: %s", data_source.name)
    connection = get_connection(data_source)

    # test connection with the credentials
    logger.info("Testing connection with the credentials. %s", data_source.name)
    if not connection.test_connection():
        logger.exception("Invalid connection data. %s", data_source.name)
        raise HTTPException(status_code=400, detail="Invalid connection data")

    logger.info("Creating data source in the database. %s", data_source.name)
    data_source = crud.create_data_source(db=db, data_source=data_source, user_id=current_user.id)
    return data_source


@app.post("/metadata/")
def get_metadata_data_sources(model: schemas.DataSourceGetMetadata, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    data_source_id = model.data_source_id

    # get metadata to db
    logger.info("Getting metadata for data source: %s", data_source_id)
    tables_columns, database_name = get_metadata(model.data_source_id, current_user.id, db)

    # generate column description using LLM
    logger.info("Generating column description using LLM")
    for table_name, columns in tables_columns.items():
        logger.info(f"Generating column description for table: {table_name=}")
        for column in columns:
            logger.info(f"Generating column description for column: {table_name=}, {column=}")
            column["description"] = generate_column_description(column, table_name)

    # save metadata to db
    logger.info("Saving metadata to the database")
    save_metadata(data_source_id, current_user.id, database_name, tables_columns, db)

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
    indexing(data_source_id, current_user.id, db)

    return {"message": "Getting metadata completed."}


@app.get("/metadata/query/")
def query_data_sources(query: str, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = storage_client.query(query, top_k=10)
    logger.info(f"Search result for {query} is : {result}")

    response_with_duplicated_tables = [
        {
            "data_source_id": r.metadata.get("data_source_id"),
            "data_source_name": crud.get_data_source(db, r.metadata.get("data_source_id"), user_id=current_user.id).name,
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
        data_source = crud.get_data_source(db, data_source_id=data_source_id, user_id=current_user.id)

        try:
            connection = get_connection(data_source)
            table_information = crud.get_table(db, data_source_id, table_name, current_user.id)
            columns = [col["column_name"] for col in table_information.table_info.get("columns")]
            sample_data = connection.select_table(table_name, limit=5)
            df = pd.DataFrame(sample_data, columns=columns)
        except Exception as e:
            logger.error("Failed to get sample data for table: %s", table_name)
            logger.exception(e)
            continue

        binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
        for column in binary_columns:
            df[column] = df[column].apply(encode_binary)

        r["sample_data"] = df.to_json(orient="records")

        logger.info(f"r: {r}")

    return response


@app.delete("/metadata/")
def delete_vector_db(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info("Clearing VectorDB")
    storage_client.clear()
    storage_client_join.clear()
    logger.info("Clearing Database")
    crud.clear_database_table_information(db)
    return {"message": "Database and VectorDB are cleared."}


@app.post("/joinable_table/indexing/")
def post_joinable_table_indexing(body: schemas.JoinableTableIndexingCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    data_source_id = body.data_source_id
    logger.info("Indexing data source: %s", data_source_id)

    indexing(data_source_id, current_user.id, db)

    return {"message": "Joinable data index created."}


@app.post("/joinable_table/join_data/")
def post_joinable_table_join_data(body: schemas.JoinableTableJoinData, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info("Joining data")
    data_source_id = body.data_source_id
    table_name = body.table_name
    merged_df, joinable_info = join_data(data_source_id, current_user.id, table_name, db)

    response_body = {"data": merged_df.to_json(orient="records"), "joinable_info": joinable_info}

    return response_body


@app.exception_handler(Exception)
def exception_handler(request, exc):
    logger.exception(exc)
    return {
        "message": "Internal Server Error",
        "detail": str(exc)
    }, 200


@app.post("/find_schema_matching/", response_model=schemas.SchemaMatchingResult)
def post_find_schema_matching(target_file: UploadFile = File(...), source_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)) -> dict:
    target_df = pd.read_csv(target_file.file)
    target_name = target_file.filename
    source_df = pd.read_csv(source_file.file)
    source_name = source_file.filename

    matching = find_schema_matching(target_name, target_df, source_name, source_df)

    target_data_matched_columns = list(matching.keys())
    tmp = []
    for v in matching.values():
        tmp += v
    source_data_matched_columns = list(set(tmp))

    response = {
        "target_data_columns": target_df.columns.tolist(),
        "target_data_matched_columns": target_data_matched_columns,
        "source_data_columns": source_df.columns.tolist(),
        "source_data_matched_columns": source_data_matched_columns,
        "matching": matching
    }

    return response


@app.post("/find_data_matching/")
def post_find_data_matching(matching: str = Form(...), target_file: UploadFile = File(...), source_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):
    matching_dict = json.loads(matching)

    target_df = pd.read_csv(target_file.file)
    source_df = pd.read_csv(source_file.file)

    data_matching_result = find_data_matching(target_df, source_df, matching_dict)

    pair_columns = ["__target_index", "__source_index"]
    pair_df = pd.DataFrame(data_matching_result, columns=pair_columns)
    merged_df = target_df.merge(pair_df, left_index=True, right_on="__target_index", how="left")
    for col in source_df.columns:
        col_tmp = col
        if col_tmp in merged_df.columns:
            col_tmp = col_tmp + "_source"
        merged_df[col_tmp] = merged_df["__source_index"].map(source_df[col])
    
    merged_df = merged_df.drop(columns=pair_columns, axis=1)

    # DataFrameをCSV形式に変換
    buffer = StringIO()
    merged_df.to_csv(buffer, index=False)
    buffer.seek(0)

    # CSVファイルをストリーミングレスポンスとして返す
    response = StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    return response
