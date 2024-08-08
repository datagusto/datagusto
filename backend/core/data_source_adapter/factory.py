from logging import getLogger
from typing import TYPE_CHECKING

from .adapters.file import FileDataSource
from .adapters.sql.bigquery import BigQueryAdapter
from .adapters.sql.duckdb import DuckDBAdapter
from .adapters.sql.mysql import MySqlAdapter
from .adapters.sql.oracle import OracleAdapter
from .adapters.sql.postgres import PostgreSqlAdapter
from .adapters.sql.sqlite import SqliteAdapter
from .types import DataSourceType

if TYPE_CHECKING:
    from .adapters.base import DataSourceBase

logger = getLogger("uvicorn.app")

ADAPTERS = {
    DataSourceType.PostgreSQL: PostgreSqlAdapter,
    DataSourceType.BigQuery: BigQueryAdapter,
    DataSourceType.Snowflake: None,
    DataSourceType.Redshift: None,
    DataSourceType.Databricks: None,
    DataSourceType.DuckDB: DuckDBAdapter,
    DataSourceType.MicrosoftSQLServer: None,
    DataSourceType.MongoDB: None,
    DataSourceType.Oracle: OracleAdapter,
    DataSourceType.SAPHana: None,
    DataSourceType.SQLite: SqliteAdapter,
    DataSourceType.MySQL: MySqlAdapter,
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
    def __init__(self, adapter_name: str, name: str, description: str, connection: dict) -> None:
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
