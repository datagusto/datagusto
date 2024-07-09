from typing import Optional

from pydantic import BaseModel


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


class OracleConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str
    schema: Optional[str]

    @property
    def dsn(self):
        return f"{self.host}:{self.port}/{self.dbname}"


class FileConfig(BaseModel):
    file_type: str
    saved_name: str

