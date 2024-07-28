from logging import getLogger

from sqlalchemy import create_engine

from .base import SqlBase
from ...config import PostgreSqlConfig

logger = getLogger()

TABLES_SQL = """
SELECT table_name FROM information_schema.tables
WHERE table_schema='{database_schema}'
    AND table_type='BASE TABLE'
    AND table_catalog='{database_name}'
"""

COLUMN_INFORMATION_SQL = """
SELECT column_name, data_type AS column_type, '' AS extra, '' AS comment FROM information_schema.columns
WHERE table_schema = '{database_schema}'
    AND table_name   = '{table_name}'
    AND table_catalog='{database_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SELECT
    kcu.column_name,
    ccu.table_name AS referenced_table_name,
    ccu.column_name AS referenced_column_name
FROM
    information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY'
    AND tc.table_name='{table_name}'
    AND tc.table_schema='{database_schema}'
    AND tc.table_catalog='{database_name}'
"""


class PostgreSqlAdapter(SqlBase):

    def post_init(self) -> None:
        self.sql_config = PostgreSqlConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL.format(
            database_schema=self.sql_config.schema,
            database_name=self.sql_config.database
        )
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
            database_name=self.sql_config.database
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
            database_name=self.sql_config.database
        )
