import os
from logging import getLogger
from typing import Union

from fastapi import HTTPException

import schemas
from adapters.mysql import MySQLConnection
from adapters.types import DataSourceType


logger = getLogger("uvicorn.app")


def get_connection(data_source: Union[schemas.DataSourceBase, schemas.DataSource]):
    config = data_source.connection
    if not config:
        raise HTTPException(status_code=400, detail="Connection data is required")

    connection = None
    try:
        if data_source.type == DataSourceType.MySQL:
            if isinstance(data_source, schemas.DataSource):
                logger.debug("Creating MySQL connection: data_source id=%s", data_source.id)
            else:
                logger.debug("Creating MySQL connection: data_source name=%s", data_source.name)
            connection = MySQLConnection(
                owner_id=data_source.owner_id,
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
