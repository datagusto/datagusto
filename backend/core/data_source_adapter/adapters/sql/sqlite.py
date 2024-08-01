from logging import getLogger

from sqlalchemy import create_engine

from ...config import MySqlConfig, SqliteConfig
from .base import SqlBase

logger = getLogger()

TABLES_SQL = """
SELECT name 
FROM sqlite_master 
WHERE type='table' 
    AND name NOT LIKE 'sqlite_%'
ORDER BY name
"""

COLUMN_INFORMATION_SQL = """
SELECT 
    name as 'column_name',
    type as 'column_type',
    CASE WHEN pk = 1 THEN 'PRIMARY KEY' 
         WHEN pk > 1 THEN 'PRIMARY KEY(' || pk || ')' 
         ELSE '' END ||
    CASE WHEN `notnull` = 1 THEN ' NOT NULL' ELSE '' END ||
    CASE WHEN dflt_value IS NOT NULL THEN ' DEFAULT ' || dflt_value ELSE '' END
    as 'extra',
    '' as 'comment'
FROM pragma_table_info('{table_name}')
"""

# get relationship information from information_schema
RELATIONSHIP_INFORMATION_SQL = """
SELECT 
    "from" as column_name,
    "table" as referenced_table_name,
    "to" as referenced_column_name
FROM pragma_foreign_key_list('{table_name}')
"""


class SqliteAdapter(SqlBase):

    def validate_config(self) -> bool:
        try:
            SqliteConfig(**self.config)
        except Exception:
            return False
        return True

    def post_init(self) -> None:
        self.sql_config = SqliteConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            table_name="{table_name}",
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            table_name="{table_name}",
        )
