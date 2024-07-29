from logging import getLogger

from sqlalchemy import create_engine

from ...config import OracleConfig
from .base import SqlBase

logger = getLogger()

TABLES_SQL = """
SELECT TABLE_NAME
FROM user_tables
WHERE user_tables.TABLESPACE_NAME = '{tablespace_name}'
"""

COLUMN_INFORMATION_SQL = """
SELECT
    COLUMN_NAME AS "column_name",
    DATA_TYPE AS "column_type",
    '' AS "extra",
    '' AS "comment"
FROM ALL_TAB_COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    AND owner = '{user_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SELECT UCC2.COLUMN_NAME AS "column_name",
       UCC.TABLE_NAME AS "referenced_table_name",
       UCC.COLUMN_NAME AS "referenced_column_name"
   FROM (SELECT TABLE_NAME, CONSTRAINT_NAME, R_CONSTRAINT_NAME, CONSTRAINT_TYPE FROM USER_CONSTRAINTS) UC,
        (SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM USER_CONS_COLUMNS) UCC,
        (SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM USER_CONS_COLUMNS) UCC2
   WHERE UC.R_CONSTRAINT_NAME = UCC.CONSTRAINT_NAME
     AND UC.CONSTRAINT_NAME = UCC2.CONSTRAINT_NAME
     AND uc.constraint_type = 'R'
     AND UC.TABLE_NAME = '{table_name}'
"""


class OracleAdapter(SqlBase):
    def post_init(self) -> None:
        self.sql_config = OracleConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL.format(tablespace_name=self.sql_config.schema.upper())
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            table_name="{table_name}",
            user_name=self.sql_config.username.upper(),
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
            database_name=self.sql_config.database,
        )

    def get_all_tables(self) -> list[str]:
        all_table_names = super().get_all_tables()

        # filter out system tables
        table_names = []
        for table_name in all_table_names:
            if (
                table_name.startswith("BIN$")
                or table_name.startswith("MVIEW$_")
                or table_name.startswith("AQ$_")
                or table_name.startswith("LOGMNRGGC_")
                or table_name.startswith("LOGMNR_")
                or table_name.startswith("ROLLING$")
                or table_name.startswith("LOGSTDBY$")
            ):
                continue
            if table_name in [
                "HELP",
                "SCHEDULER_PROGRAM_ARGS_TBL",
                "SCHEDULER_JOB_ARGS_TBL",
                "SQLPLUS_PRODUCT_PROFILE",
            ]:
                continue
            table_names.append(table_name)
        return table_names

    def select_column(self, table: str, column: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT {column} FROM {table} FETCH FIRST {limit} ROWS ONLY"  # noqa: S608
        return self.execute_query(query)

    def select_table(self, table: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT * FROM {table} FETCH FIRST {limit} ROWS ONLY"  # noqa: S608
        return self.execute_query(query)
