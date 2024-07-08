from logging import getLogger
from typing import Any

import oracledb

from .base import DataSourceBase
from ..config import OracleConfig

logger = getLogger("uvicorn.app")


TABLES_SQL = """
SELECT TABLE_NAME
FROM user_tables
WHERE user_tables.TABLESPACE_NAME = '{tablespace_name}'
"""

COLUMN_INFORMATION_SQL = """
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    DATA_LENGTH,
    DATA_PRECISION,
    DATA_SCALE
FROM ALL_TAB_COLUMNS
    WHERE TABLE_NAME = '{table_name}' 
    AND owner = '{user_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SELECT UC.TABLE_NAME,
       UCC2.COLUMN_NAME,
       UCC.TABLE_NAME,
       UCC.COLUMN_NAME
   FROM (SELECT TABLE_NAME, CONSTRAINT_NAME, R_CONSTRAINT_NAME, CONSTRAINT_TYPE FROM USER_CONSTRAINTS) UC,
        (SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM USER_CONS_COLUMNS) UCC,
        (SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM USER_CONS_COLUMNS) UCC2
   WHERE UC.R_CONSTRAINT_NAME = UCC.CONSTRAINT_NAME
     AND UC.CONSTRAINT_NAME = UCC2.CONSTRAINT_NAME
     AND uc.constraint_type = 'R'
     AND UC.TABLE_NAME = '{table_name}'
"""

class OracleDataSource(DataSourceBase):
    connection: Any = None
    cursor: Any = None
    schema: str = None

    def post_init(self):
        self.schema = self.config.pop("schema", "system")

    def validate_config(self) -> bool:
        # validate the config by initializing the MySQLConfig pydantic class
        try:
            OracleConfig(**self.config)
        except Exception:
            logger.exception("Invalid MySQL config: %s", self.config)
            return False
        return True

    def test_connection(self) -> bool:
        try:
            _connection = oracledb.connect(
                user=self.config["user"],
                password=self.config["password"],
                dsn=f'{self.config["host"]}:{self.config["port"]}/{self.config["dbname"]}'
            )
            _connection.close()
        except oracledb.DatabaseError:
            return False
        return True

    def set_cursor(self):
        if not self.connection:
            self.connection = oracledb.connect(
                user=self.config["user"],
                password=self.config["password"],
                dsn=f'{self.config["host"]}:{self.config["port"]}/{self.config["dbname"]}'
            )
        if not self.cursor:
            self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    def get_database_name(self):
        return self.config["dbname"]

    def get_all_tables(self):
        self.set_cursor()
        self.cursor.execute(TABLES_SQL.format(tablespace_name=self.schema.upper()))
        tables = self.cursor.fetchall()
        self.close()
        table_names = [table[0] for table in tables]
        user_tables = []
        for table_name in table_names:
            if table_name.startswith("BIN$") or table_name.startswith("MVIEW$_") or table_name.startswith("AQ$_"):
                continue
            if table_name in ["HELP","SCHEDULER_PROGRAM_ARGS_TBL","SCHEDULER_JOB_ARGS_TBL","SQLPLUS_PRODUCT_PROFILE"]:
                continue
            user_tables.append(table_name)
        return user_tables

    def get_all_columns(self):
        tables = self.get_all_tables()
        self.set_cursor()
        all_columns = {}
        for table in tables:
            logger.debug("Getting column information (metadata) of table :" + table)
            self.cursor.execute(COLUMN_INFORMATION_SQL.format(
                user_name=self.config["user"].upper(),
                table_name=table.upper())
            )
            columns = self.cursor.fetchall()
            self.cursor.execute(RELATIONSHIP_INFORMATION_SQL.format(
                table_name=table.upper())
            )
            relationships = self.cursor.fetchall()

            for column in columns:
                (column_name, data_type, data_length, data_precision, data_scale) = column
                column_info = {
                    "column_name": column_name,
                    "column_type": data_type,
                    "data_length": data_length,
                    "data_precision": data_precision,
                    "data_scale": data_scale
                }

                # Using next() with a generator expression to find the first matching relationship or None
                _, _, ref_table_name, ref_column_name = next((r for r in relationships if column_name == r[1]),
                                                          (None, None, None, None))
                if ref_table_name:
                    column_info.update({
                        "referenced_table_name": ref_table_name,
                        "referenced_column_name": ref_column_name
                    })
                    relationships.remove((table, column_name, ref_table_name, ref_column_name))

                all_columns.setdefault(table, []).append(column_info)
        self.close()
        return all_columns

    def execute_query(self, query: str):
        self.set_cursor()
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close()
        return data

    def select_column(self, table: str, column: str, limit: int = 1000):
        query = f"SELECT {column} FROM {table} FETCH FIRST {limit} ROWS ONLY"
        return self.execute_query(query)

    def select_table(self, table: str, limit: int = 1000):
        query = f"SELECT * FROM {table} FETCH FIRST {limit} ROWS ONLY"
        return self.execute_query(query)
