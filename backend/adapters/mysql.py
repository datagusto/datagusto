from logging import getLogger

import mysql.connector
from pydantic import BaseModel

from .connection import Connection

logger = getLogger("uvicorn.app")


class MySQLConfig(BaseModel):
    host: str
    port: int = 3306
    username: str
    password: str
    database: str


class MySQLConnection(Connection):
    connection: "MySQLConnectionAbstract" = None
    cursor: "MySQLCursorAbstract" = None

    def validate_config(self) -> bool:
        # validate the config by initializing the MySQLConfig pydantic class
        try:
            MySQLConfig(**self.config)
        except Exception:
            logger.exception("Invalid MySQL config: %s", self.config)
            return False
        return True

    def test_connection(self) -> bool:
        try:
            _connection = mysql.connector.connect(**self.config)
            _connection.close()
        except mysql.connector.Error:
            return False
        return True

    def set_cursor(self):
        if not self.connection:
            self.connection = mysql.connector.connect(**self.config)
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
        tables = self.get_all_tables()
        self.set_cursor()
        all_columns = {}
        for table in tables:
            # "show full columns from table_name" shows privileges and comment
            # self.cursor.execute(f"DESCRIBE {table_name}")
            self.cursor.execute(f"show full columns from {table}")
            columns = self.cursor.fetchall()
            all_columns[table] = [
                {
                    "column_name": column[0],
                    "data_type": column[1],
                    # "collation": column[2],
                    # "is_nullable": column[3],
                    # "key": column[4],
                    # "default_value": column[5],
                    "extra": column[6],
                    # "privileges": column[7],
                    "comment": column[8]
                } for column in columns]
        self.close()
        return all_columns
    
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
