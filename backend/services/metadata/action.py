from logging import getLogger

import pandas as pd
from sqlalchemy.orm import Session

from core.abac.check import get_accessible_resource_ids
from core.data_source_adapter.factory import DataSourceFactory
from core.vector_db_adapter.factory import VectorDatabaseFactory
from database.crud import data_source as data_source_crud
from database.crud import metadata as metadata_crud
from schemas import metadata as metadata_schema

from ..common import encode_binary
from .llm import generate_column_description, generate_docs_from_columns

logger = getLogger("uvicorn.app")


def get_and_save_metadata(db: Session, data_source_id: int, user_id: int) -> None:
    # get metadata to db
    logger.info("Getting metadata for data source: %s", data_source_id)
    tables_columns, database_name = _get_metadata(data_source_id, user_id, db)

    # generate column description using LLM
    logger.info("Generating column description using LLM")
    for table_name, columns in tables_columns.items():
        logger.info(f"Generating column description for table: {table_name=}")
        for column in columns:
            logger.info(f"Generating column description for column: {table_name=}, {column=}")
            column["description"] = generate_column_description(column, table_name)
            logger.info(f"Generated column description: {column['description']}")

    # save metadata to db
    if len(tables_columns) > 0:
        logger.info("Saving metadata to the database")
        _save_metadata(data_source_id, user_id, database_name, tables_columns, db)
    else:
        logger.info("No metadata to save to the database")

    # save embedded metadata to vectordb
    logger.info("Saving metadata to VectorDB")
    all_columns = []
    for table_name, columns in tables_columns.items():
        all_columns.extend(
            [
                {
                    "table_name": table_name,
                }
                | column
                for column in columns
            ],
        )
    docs = generate_docs_from_columns(all_columns, database_name, data_source_id, user_id)
    if len(docs) > 0:
        factory = VectorDatabaseFactory()
        vector_db_client = factory.get_vector_database()
        vector_db_client.save(docs)
    else:
        logger.info("No metadata to save to VectorDB")


def query_metadata(db: Session, query: str, user_id: int) -> list[dict]:
    shared_data_source_ids = get_accessible_resource_ids(db, user_id)
    factory = VectorDatabaseFactory()
    vector_db_client = factory.get_vector_database()
    result = vector_db_client.query(query, user_id=user_id, shared_data_source_ids=shared_data_source_ids, top_k=10)
    logger.info(f"Search result for {query} is : {result}")

    data_sources = {
        r.metadata.get("data_source_id"): data_source_crud.get_data_source(
            db,
            r.metadata.get("data_source_id"),
            user_id=user_id,
        ).name
        for r in result
    }

    response_with_duplicated_tables = [
        {
            "data_source_id": r.metadata.get("data_source_id"),
            "data_source_name": data_sources[r.metadata.get("data_source_id")],
            "database_name": r.metadata.get("database_name"),
            "table_name": r.metadata.get("table_name"),
            "column_description": [r.page_content],
        }
        for r in result
    ]

    # Combine responses with the same table name
    response = {}
    for r in response_with_duplicated_tables:
        table_name = r["table_name"]
        if table_name not in response:
            response[table_name] = r
        else:
            response[table_name]["column_description"].extend(r["column_description"])

    response = _get_sample_data_from_tables(db, list(response.values()), user_id)

    return response


def _get_metadata(data_source_id: int, user_id: int, db: Session) -> tuple[dict, str]:
    logger.debug("Starting to get metadata from data source: data_source_id=%s", data_source_id)
    data_source = data_source_crud.get_data_source(db, data_source_id=data_source_id, user_id=user_id)

    factory = DataSourceFactory(
        adapter_name=data_source.type,
        name=data_source.name,
        description=data_source.description,
        connection=data_source.connection,
    )
    connection = factory.get_data_source()
    logger.debug(
        "Getting all column data (metadata) from the database. data_source_id=%s, database_name=%s",
        data_source_id,
        connection.get_database_name(),
    )
    all_columns = connection.get_all_columns()
    logger.debug(f"all_columns: {all_columns}")

    return all_columns, connection.get_database_name()


def _save_metadata(data_source_id: int, user_id: int, database_name: str, all_columns: dict, db: Session) -> None:
    # save to database
    logger.debug(
        "Generating database column instance to save to the database. data_source_id=%s, database_name=%s",
        data_source_id,
        database_name,
    )
    database_information = metadata_schema.DatabaseInformationCreate(
        data_source_id=data_source_id,
        database_name=database_name,
        schema_name=database_name,
    )
    table_information = []
    for table_name, columns in all_columns.items():
        table_information.append(
            metadata_schema.TableInformationCreate(
                data_source_id=data_source_id,
                table_name=table_name,
                table_info={
                    "database_name": database_name,
                    "schema_name": database_name,
                    "table_name": table_name,
                    "columns": columns,
                },
            ),
        )
    database_information.table_information = table_information

    logger.debug(
        "Saving database column information to the database. data_source_id=%s, database_name=%s",
        data_source_id,
        database_name,
    )
    metadata_crud.create_database_information(db, database_information, user_id)


def _get_sample_data_from_tables(db: Session, response: list, user_id: int) -> list[dict]:
    # get sample data for each table
    for r in response:
        data_source_id = r["data_source_id"]
        table_name = r["table_name"]
        data_source = data_source_crud.get_data_source(db, data_source_id=data_source_id, user_id=user_id)

        try:
            factory = DataSourceFactory(
                adapter_name=data_source.type,
                name=data_source.name,
                description=data_source.description,
                connection=data_source.connection,
            )
            connection = factory.get_data_source()
            table_information = data_source_crud.get_table(db, data_source_id, table_name, user_id)
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


def delete_metadata(db: Session, data_source_id: int, user_id: int) -> None:
    logger.debug("Deleting metadata from the database. data_source_id=%s", data_source_id)
    metadata_crud.delete_database_information(db, data_source_id, user_id)


def delete_all_metadata(db: Session) -> None:
    logger.info("Clearing VectorDB")
    factory = VectorDatabaseFactory()
    vector_db_client = factory.get_vector_database()
    vector_db_join_client = factory.get_vector_database_join()
    vector_db_client.clear()
    vector_db_join_client.clear()
    logger.info("Clearing Database")
    metadata_crud.clear_database_table_information(db)
