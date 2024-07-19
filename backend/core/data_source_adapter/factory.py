from logging import getLogger

from .adapters.base import DataSourceBase
from .adapters.file import FileDataSource
from .adapters.mysql import MySQLDataSource
from .adapters.oracle import OracleDataSource
from .adapters.postgres import PostgreSQLDataSource
from .types import DataSourceType

logger = getLogger("uvicorn.app")

ADAPTERS = {
    DataSourceType.PostgreSQL: PostgreSQLDataSource,
    DataSourceType.BigQuery: None,
    DataSourceType.Snowflake: None,
    DataSourceType.Redshift: None,
    DataSourceType.Databricks: None,
    DataSourceType.DuckDB: None,
    DataSourceType.MicrosoftSQLServer: None,
    DataSourceType.MongoDB: None,
    DataSourceType.Oracle: OracleDataSource,
    DataSourceType.SAPHana: None,
    DataSourceType.SQLite: None,
    DataSourceType.MySQL: MySQLDataSource,
    DataSourceType.Gorgias: None,
    DataSourceType.SpreadSheet: None,
    DataSourceType.Notion: None,
    DataSourceType.Shopify: None,
}

FILE_ADAPTERS = {
    DataSourceType.CSVFile: FileDataSource,
    DataSourceType.ExcelFile: FileDataSource,
    DataSourceType.TabularFile: FileDataSource,
}


class DataSourceFactory:
    def __init__(self, adapter_name: str, name: str, description: str, connection: dict):
        if adapter_name not in ADAPTERS and adapter_name not in FILE_ADAPTERS:
            raise ValueError(f"{adapter_name} is not a valid data source type.")
        self.adapter_name = adapter_name
        self.name = name
        self.description = description
        self.connection = connection

    def get_data_source(self) -> "DataSourceBase":
        logger.debug(f"Creating {self.adapter_name} connection: data_source name={self.name}")
        adapter = ADAPTERS[self.adapter_name]
        return adapter(name=self.name, description=self.description, config=self.connection)

    def get_data_source_file(self) -> FileDataSource:
        logger.debug(f"Creating {self.adapter_name} file: data_source name={self.name}")
        adapter = FILE_ADAPTERS[self.adapter_name]
        return adapter(name=self.name, description=self.description, config=self.connection)
