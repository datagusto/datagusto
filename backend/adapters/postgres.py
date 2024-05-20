from logging import getLogger
from typing import Any

import psycopg2

from .connection import Connection
from .types import PostgreSQLConfig

logger = getLogger("uvicorn.app")


class PostgreSQLConnection(Connection):
    connection: Any = None
    cursor: Any = None

    def validate_config(self) -> bool:
        # validate the config by initializing the MySQLConfig pydantic class
        try:
            PostgreSQLConfig(**self.config)
        except Exception:
            logger.exception("Invalid MySQL config: %s", self.config)
            return False
        return True

    def test_connection(self) -> bool:
        try:
            _connection = psycopg2.connect(**self.config)
            _connection.close()
        except psycopg2.DatabaseError:
            return False
        return True

    def set_cursor(self):
        if not self.connection:
            self.connection = psycopg2.connect(**self.config)
        if not self.cursor:
            self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    def get_database_name(self):
        return self.config["database"]

    def get_all_tables(self):
        self.set_cursor()
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        self.close()
        return [table[0] for table in tables]

    def get_all_columns(self):
        # TODO: implement this method
        return {}

    def execute_query(self, query: str):
        self.set_cursor()
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close()
        return data

    def select_column(self, table: str, column: str, limit: int = 1000):
        self.set_cursor()
        self.cursor.execute(f"SELECT `{column}` FROM {table} LIMIT {limit}")
        data = self.cursor.fetchall()
        self.close()
        return data
    
    def select_table(self, table: str, limit: int = 1000):
        self.set_cursor()
        self.cursor.execute(f"SELECT * FROM {table} LIMIT {limit}")
        data = self.cursor.fetchall()
        self.close()
        return data
