import os
from logging import getLogger
from typing import Union

from fastapi import HTTPException

import schemas
from .file import FileConnection
from .mysql import MySQLConnection
from .postgres import PostgreSQLConnection
from .types import DataSourceType


logger = getLogger("uvicorn.app")


def get_connection(data_source: Union[schemas.DataSourceBase, schemas.DataSource]):
    config = data_source.connection
    if not config:
        raise HTTPException(status_code=400, detail="Connection data is required")

    connection = None
    try:
        message = f"Creating {{DATA_SOURCE}} connection: data_source name={data_source.name}"
        if isinstance(data_source, schemas.DataSource):
            message = f"Creating {{DATA_SOURCE}} connection: data_source id={data_source.id}"
        if data_source.type == DataSourceType.MySQL:
            logger.debug(message.format(DATA_SOURCE="MySQL"))
            connection = MySQLConnection(
                name=data_source.name,
                description=data_source.description,
                config=data_source.connection
            )
        if data_source.type == DataSourceType.File:
            logger.debug(message.format(DATA_SOURCE="File"))
            connection = FileConnection(
                name=data_source.name,
                description=data_source.description,
                config=data_source.connection
            )
        if data_source.type == DataSourceType.PostgreSQL:
            logger.debug(message.format(DATA_SOURCE="PostgreSQL"))
            connection = PostgreSQLConnection(
                name=data_source.name,
                description=data_source.description,
                config=data_source.connection
            )
    except Exception as e:
        logger.exception("Error creating connection: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    if not connection:
        raise HTTPException(status_code=400, detail="Invalid connection type")
    return connection
