from logging import getLogger

from sqlalchemy import create_engine

from ...config import MySqlConfig
from .base import SqlBase

logger = getLogger()

COLUMN_INFORMATION_SQL = """
SELECT
    COLUMN_NAME as 'column_name', COLUMN_TYPE as 'column_type', EXTRA as 'extra', COLUMN_COMMENT as 'comment'
FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA = '{database_name}' AND
    TABLE_NAME = '{table_name}'
"""

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


class MySqlAdapter(SqlBase):
    def post_init(self) -> None:
        self.sql_config = MySqlConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            database_name=self.get_database_name(),
            table_name="{table_name}",
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_name=self.get_database_name(),
            table_name="{table_name}",
        )
