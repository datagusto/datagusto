from logging import getLogger

from fastapi import HTTPException

import schemas
from adapters.mysql import MySQLConnection
from database import DataSourceType


logger = getLogger("uvicorn.app")


def get_connection(type: DataSourceType, config: dict):
    if not config:
        raise HTTPException(status_code=400, detail="Connection data is required")

    connection = None
    try:
        if type == schemas.DataSourceType.MySQL:
            connection = MySQLConnection(config=config)
    except Exception as e:
        logger.exception("Error creating connection: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    if not connection:
        raise HTTPException(status_code=400, detail="Invalid connection type")
    return connection

