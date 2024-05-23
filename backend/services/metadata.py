import os
from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas
from adapters.connections import get_connection
from database import crud

logger = getLogger("uvicorn.app")


def get_metadata(data_source_id: int, user_id: int, db: Session):
    logger.debug("Starting to get metadata from data source: data_source_id=%s", data_source_id)
    data_source: schemas.DataSource = crud.get_data_source(db, data_source_id=data_source_id, user_id=user_id)
    if not data_source:
        logger.warning("data_source_id: %s not found", data_source_id)
        raise HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")

    connection = get_connection(data_source)
    logger.debug("Getting all column data (metadata) from the database. data_source_id=%s, database_name=%s",
                 data_source_id, connection.get_database_name())
    all_columns = connection.get_all_columns()
    logger.debug(f"all_columns: {all_columns}")

    return all_columns, connection.get_database_name()


def save_metadata(data_source_id: int, user_id: int, database_name: str, all_columns: dict, db: Session):
    # save to database
    logger.debug("Generating database column instance to save to the database. data_source_id=%s, database_name=%s",
                 data_source_id, database_name)
    database_information = schemas.DatabaseInformationCreate(
        data_source_id=data_source_id,
        database_name=database_name,
        schema_name=database_name
    )
    table_information = []
    for table_name, columns in all_columns.items():
        table_information.append(schemas.TableInformationCreate(
            data_source_id=data_source_id,
            table_name=table_name,
            table_info={
                "database_name": database_name,
                "schema_name": database_name,
                "table_name": table_name,
                "columns": columns
            }
        ))
    database_information.table_information = table_information

    logger.debug("Saving database column information to the database. data_source_id=%s, database_name=%s",
                 data_source_id, database_name)
    crud.create_database_information(db, database_information, user_id)
