from logging import getLogger

from sqlalchemy import create_engine

from ...config import MsSqlConfig
from .base import SqlBase

logger = getLogger()

TABLES_SQL = """
SELECT TABLE_NAME FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND TABLE_SCHEMA = '{database_schema}'
  AND TABLE_CATALOG = '{database_name}'
  AND TABLE_NAME NOT LIKE 'spt_%'
  AND TABLE_NAME != 'MSreplication_options'
"""

COLUMN_INFORMATION_SQL = """
SELECT
    c.column_name,
    c.data_type AS column_type,
    CASE
        WHEN c.is_nullable = 'YES' THEN 'nullable'
        ELSE 'non-nullable'
    END AS extra,
    ISNULL(CAST(prop.value AS NVARCHAR(MAX)), '') AS comment
FROM
    information_schema.columns c
LEFT JOIN
    sys.tables t ON c.table_name = t.name
LEFT JOIN
    sys.schemas s ON c.table_schema = s.name
LEFT JOIN
    sys.extended_properties prop ON prop.major_id = t.object_id
        AND prop.minor_id = c.ordinal_position
        AND prop.class = 1  -- Object or column
        AND prop.name = 'MS_Description'
WHERE
    c.table_schema = '{database_schema}'
    AND c.table_name = '{table_name}'
    AND c.table_catalog = '{database_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SELECT
    COL_NAME(fc.parent_object_id, fc.parent_column_id) AS column_name,
    OBJECT_NAME(f.referenced_object_id) AS referenced_table_name,
    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS referenced_column_name
FROM
    sys.foreign_keys AS f
INNER JOIN
    sys.foreign_key_columns AS fc ON f.object_id = fc.constraint_object_id
INNER JOIN
    sys.tables AS t ON t.object_id = f.parent_object_id
INNER JOIN
    sys.schemas AS s ON s.schema_id = t.schema_id
WHERE
    OBJECT_NAME(f.parent_object_id) = '{table_name}'
    AND s.name = '{database_schema}'
    AND DB_NAME() = '{database_name}'
"""


class MsSqlAdapter(SqlBase):
    def post_init(self) -> None:
        self.sql_config = MsSqlConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL.format(
            database_schema=self.sql_config.schema,
            database_name=self.sql_config.database,
        )
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
            database_name=self.sql_config.database,
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema,
            table_name="{table_name}",
            database_name=self.sql_config.database,
        )

    def select_column(self, table: str, column: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT TOP {limit} {column} FROM {table}"  # noqa: S608
        return self.execute_query(query)

    def select_table(self, table: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT TOP {limit} * FROM {table}"  # noqa: S608
        return self.execute_query(query)
