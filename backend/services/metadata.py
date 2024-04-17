from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from adapters.mysql import MySQLConnection

logger = getLogger("uvicorn.app")


def get_metadata(data_source_id: int, db: Session):
    logger.debug("Starting to get metadata from data source: data_source_id=%s", data_source_id)
    data_source = crud.get_data_source(db, data_source_id=data_source_id)
    if not data_source:
        logger.warning("data_source_id: %s not found", data_source_id)
        raise HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")

    connection = None
    if data_source.type == schemas.DataSourceType.MySQL:
        logger.debug("Creating MySQL connection: data_source_id=%s", data_source_id)
        connection = MySQLConnection(config=data_source.connection)

    logger.debug("Getting all column data (metadata) from the database. data_source_id=%s, database_name=%s",
                 data_source_id, connection.get_database_name())
    all_columns = connection.get_all_columns()
    logger.debug(f"all_columns: {all_columns}")

    return all_columns, connection.get_database_name()


def save_metadata(data_source_id: int, database_name: str, all_columns: dict, db: Session):
    logger.debug("Generating database column instance to save to the database. data_source_id=%s, database_name=%s",
                 data_source_id, database_name)
    database_column_information = []
    for table_name, columns in all_columns.items():
        database_column_information.extend([
            schemas.DatabaseInformationCreate(
                data_source_id=data_source_id,
                database_name=database_name,
                table_name=table_name,
                column_name=column["column_name"],
                column_info=column
            ) for column in columns])

    logger.debug("Saving database column information to the database. data_source_id=%s, database_name=%s",
                 data_source_id, database_name)
    crud.create_database_column_information_bulk(db, database_column_information)
