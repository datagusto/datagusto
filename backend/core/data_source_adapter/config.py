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


class FileConfig(BaseModel):
    file_type: str
    saved_name: str
