import os

from pydantic import BaseModel


class SqlConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

    def connector_type(self) -> str:
        return ""

    @property
    def uri(self) -> str:
        return f"{self.connector_type()}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


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
            f"{self.connector_type()}://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/?service_name={self.database}"
        )


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
    dataset: str

    @property
    def database(self) -> str:
        return self.dataset

    @property
    def uri(self) -> str:
        return f"bigquery://{self.project_id}/{self.dataset}"


class FileConfig(BaseModel):
    file_type: str
    saved_name: str
