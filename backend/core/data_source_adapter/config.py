import os
from typing import Optional
from urllib.parse import quote_plus

from pydantic import BaseModel


class SqlConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

    def connector_type(self) -> str:
        return ""

    def encode_password(self) -> str:
        return quote_plus(self.password)

    @property
    def uri(self) -> str:
        return f"{self.connector_type()}://{self.username}:{self.encode_password()}@{self.host}:{self.port}/{self.database}"


class MySqlConfig(SqlConfig):
    def connector_type(self) -> str:
        return "mysql+mysqlconnector"


class PostgreSqlConfig(SqlConfig):
    schema: str = "public"

    def connector_type(self) -> str:
        return "postgresql+psycopg2"


class OracleConfig(SqlConfig):
    schema: str = "system"

    def connector_type(self) -> str:
        return "oracle+oracledb"
        # return "oracle+cx_oracle"

    @property
    def uri(self) -> str:
        return (
            f"{self.connector_type()}://{self.username}:{self.encode_password()}"
            f"@{self.host}:{self.port}/?service_name={self.database}"
        )


class MsSqlConfig(SqlConfig):
    schema: str = "dbo"

    def connector_type(self) -> str:
        return "mssql+pyodbc"

    @property
    def uri(self) -> str:
        _uri = super().uri
        return f"{_uri}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"


class SnowflakeConfig(SqlConfig):
    host: Optional[str] = None
    port: Optional[int] = None
    account: str
    schema: str = "public"

    def connector_type(self) -> str:
        return "snowflake"

    @property
    def uri(self) -> str:
        return f"{self.connector_type()}://{self.username}:{self.encode_password()}@{self.account}/{self.database}"


class SqlFileServerConfig(BaseModel):
    file_name: str

    @property
    def uri(self) -> str:
        datasource_base_path = os.getenv("DATASOURCE_BASE_PATH", "./datasource")
        return f"{self.connector_type()}:///{datasource_base_path}/{self.connector_type()}/{self.database}"

    @property
    def database(self) -> str:
        return self.file_name

    def connector_type(self) -> str:
        return ""


class SqliteConfig(SqlFileServerConfig):
    def connector_type(self) -> str:
        return "sqlite"


class DuckDBConfig(SqlFileServerConfig):
    schema: str = "main"

    def connector_type(self) -> str:
        return "duckdb"


class BigQueryConfig(BaseModel):
    credentials: dict
    project_id: str
    dataset_id: str

    @property
    def database(self) -> str:
        return self.dataset_id

    @property
    def uri(self) -> str:
        return f"bigquery://{self.project_id}/{self.dataset_id}"


class FileConfig(BaseModel):
    file_type: str
    saved_name: str
