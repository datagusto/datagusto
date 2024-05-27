import enum
from typing import Optional

from pydantic import BaseModel


class DataSourceType(enum.Enum):
    MySQL = "mysql"
    PostgreSQL = "postgresql"
    File = "file"
    Sap = "sap"
    SpreadSheet = "spreadsheet"
    Snowflake = "snowflake"
    BigQuery = "bigquery"


class MySQLConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

    @property
    def host_port(self):
        return f"{self.host}:{self.port}"


class PostgreSQLConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str
    schema: Optional[str]

    @property
    def host_port(self):
        return f"{self.host}:{self.port}"


class FileConfig(BaseModel):
    file_type: str
    saved_name: str
