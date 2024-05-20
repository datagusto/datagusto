from logging import getLogger

import mysql.connector

from .connection import Connection
from .types import MySQLConfig

logger = getLogger("uvicorn.app")

# SHOW FULL COLUMNS FROM TABLE_NAME shows privileges and comment (describe table_name does not show comment)
COLUMN_INFORMATION_SQL = "SHOW FULL COLUMNS FROM {table_name}"

# get relationship information from information_schema
RELATIONSHIP_INFORMATION_SQL = """
SELECT
    column_name, referenced_table_name, referenced_column_name
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_SCHEMA = '{database_name}' AND
    TABLE_NAME = '{table_name}' AND
    REFERENCED_TABLE_NAME IS NOT NULL
"""


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
            logger.debug("Getting column information (metadata) of table :" + table)
            self.cursor.execute(COLUMN_INFORMATION_SQL.format(table_name=table))
            columns = self.cursor.fetchall()
            self.cursor.execute(RELATIONSHIP_INFORMATION_SQL.format(
                database_name=self.get_database_name(), table_name=table))
            relationships = self.cursor.fetchall()

            for column in columns:
                column_name, column_type, collation, is_nullable, key, default_value, extra, privileges, comment = column
                column_info = {
                    "column_name": column_name,
                    "column_type": column_type,
                    "extra": extra,
                    "comment": comment
                }

                # Using next() with a generator expression to find the first matching relationship or None
                _, table_name, column_name = next((r for r in relationships if column_name == r[0]), (None, None, None))
                if table_name:
                    column_info.update({
                        "referenced_table_name": table_name,
                        "referenced_column_name": column_name
                    })
                    relationships.remove((column_name, table_name, column_name))

                # Using dict.setdefault to simplify the if-else block
                all_columns.setdefault(table, []).append(column_info)
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
