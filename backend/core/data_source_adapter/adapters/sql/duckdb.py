from logging import getLogger

from sqlalchemy import create_engine

from ...config import DuckDBConfig
from .base import SqlFileServerBase

logger = getLogger()

TABLES_SQL = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'main' AND table_type IN ('BASE TABLE', 'VIEW')
ORDER BY table_name
"""

COLUMN_INFORMATION_SQL = """
SELECT
    column_name,
    data_type as column_type,
    CASE
        WHEN is_nullable = 'NO' THEN 'NOT NULL'
        ELSE ''
    END ||
    CASE
        WHEN column_default IS NOT NULL THEN ' DEFAULT ' || column_default
        ELSE ''
    END as extra,
    '' as comment  -- DuckDB doesn't store column comments in information_schema
FROM
    information_schema.columns
WHERE
    table_schema = '{database_schema}' AND  -- 'main' is the default schema in DuckDB
    table_name = '{table_name}'
ORDER BY
    ordinal_position
"""

# get relationship information from information_schema
RELATIONSHIP_INFORMATION_SQL = """
SELECT
    kcu.column_name,
    kcu.table_name AS referenced_table_name,
    kcu.column_name AS referenced_column_name
FROM
    information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE
    tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name = '{table_name}'
    AND tc.table_schema = '{database_schema}'
ORDER BY
    kcu.ordinal_position
"""


class DuckDBAdapter(SqlFileServerBase):
    def post_init(self) -> None:
        self.sql_config = DuckDBConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
        )
