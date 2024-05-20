import enum

from pydantic import BaseModel


class DataSourceType(enum.Enum):
    MySQL = "mysql"
    PostgreSQL = "postgresql"


class MySQLConfig(BaseModel):
    host: str
    port: int = 3306
    username: str
    password: str
    database: str

    @property
    def host_port(self):
        return f"{self.host}:{self.port}"


class PostgreSQLConfig(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    database: str = "postgres"

    @property
    def host_port(self):
        return f"{self.host}:{self.port}"
