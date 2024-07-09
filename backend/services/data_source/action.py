import json
import uuid
from logging import getLogger
from typing import BinaryIO

import pandas as pd
from sqlalchemy.orm import Session

from core.data_source_adapter.config import FileConfig
from core.data_source_adapter.factory import DataSourceFactory
from database.crud import data_source as data_source_crud
from database.models import DataSource
from schemas import data_source as data_source_schema

from ..common import encode_binary

logger = getLogger("uvicorn.app")


def create_data_source(db: Session, data_source: data_source_schema.DataSourceCreate, user_id: int) -> DataSource:
    # initialize connection based on the data source type
    logger.info("Creating data source, and checking db connection info correct.: %s", data_source.name)

    if test_data_source_connection(data_source) is False:
        logger.exception("Invalid connection data. %s", data_source.name)
        raise Exception("Invalid connection data.")

    logger.info("Creating data source in the database. %s", data_source.name)
    return data_source_crud.create_data_source(db=db, data_source=data_source, user_id=user_id)


def create_data_source_from_file(db: Session, detail: str, file: BinaryIO, file_name: str, user_id: int) -> DataSource:
    logger.info("Creating data source from file: %s", file_name)
    detail_dict = json.loads(detail)
    file_type = detail_dict.get("file_type")
    if file_type not in ["csv"]:
        raise Exception("Only CSV or TSV files are supported")

    connection = FileConfig(
        file_type=detail_dict.get("file_type"),
        saved_name=f"{uuid.uuid4().hex}.{file_type}",
    )

    data_source = data_source_schema.DataSourceCreate(**detail_dict, connection=connection.dict())
    factory = DataSourceFactory(
        adapter_name=data_source.type,
        name=data_source.name,
        description=data_source.description,
        connection=data_source.connection,
    )
    connection = factory.get_data_source_file()

    # save file to the storage
    logger.info("Saving file to the storage: %s", file_name)
    connection.save_file(file)

    return data_source_crud.create_data_source(db=db, data_source=data_source, user_id=user_id)


def test_data_source_connection(data_source: data_source_schema.DataSourceCreate) -> bool:
    factory = DataSourceFactory(
        adapter_name=data_source.type,
        name=data_source.name,
        description=data_source.description,
        connection=data_source.connection,
    )
    connection = factory.get_data_source()
    return connection.test_connection()


def get_sample_data_from_table(db: Session, data_source_id: int, table_name: str, user_id: int) -> pd.DataFrame:
    table_information = data_source_crud.get_table(db, data_source_id, table_name, user_id)
    columns = [col["column_name"] for col in table_information.table_info.get("columns")]

    data_source = data_source_crud.get_data_source(db, data_source_id=data_source_id, user_id=user_id)
    factory = DataSourceFactory(
        adapter_name=data_source.type,
        name=data_source.name,
        description=data_source.description,
        connection=data_source.connection,
    )
    connection = factory.get_data_source()
    sample_data = connection.select_table(table_name, limit=5)
    df = pd.DataFrame(sample_data, columns=columns)

    binary_columns = df.columns[df.applymap(lambda x: isinstance(x, bytes)).any()]
    for column in binary_columns:
        df[column] = df[column].apply(encode_binary)
    return df


def delete_data_source_by_id(db: Session, data_source_id: int, user_id: int) -> bool:
    return data_source_crud.delete_data_source(db, data_source_id, user_id)
