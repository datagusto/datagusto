from logging import getLogger

from sqlalchemy import create_engine

from ...config import SnowflakeConfig
from .base import SqlBase

logger = getLogger()

TABLES_SQL = """
SELECT table_name FROM information_schema.tables
WHERE table_schema = '{database_schema}'
AND table_type = 'BASE TABLE'
AND table_catalog = '{database_name}'
"""

COLUMN_INFORMATION_SQL = """
SELECT
    column_name,
    data_type AS column_type,
    CASE
        WHEN is_nullable = 'YES' THEN 'nullable'
        ELSE 'non-nullable'
    END AS extra,
    comment
FROM information_schema.columns
WHERE table_schema = '{database_schema}'
AND table_name = '{table_name}'
AND table_catalog = '{database_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SHOW IMPORTED KEYS IN {database_name}.{database_schema}.{table_name}
"""


class SnowflakeAdapter(SqlBase):
    def validate_config(self) -> bool:
        try:
            SnowflakeConfig(**self.config)
        except Exception:
            return False
        return True

    def post_init(self) -> None:
        self.sql_config = SnowflakeConfig(**self.config)
        self.engine = create_engine(self.sql_config.uri)
        self.query_show_all_tables = TABLES_SQL.format(
            database_schema=self.sql_config.schema.upper(),
            database_name=self.sql_config.database.upper(),
        )
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema.upper(),
            table_name="{table_name}",
            database_name=self.sql_config.database.upper(),
        )
        self.query_relationship_information = RELATIONSHIP_INFORMATION_SQL.format(
            database_schema=self.sql_config.schema.upper(),
            table_name="{table_name}",
            database_name=self.sql_config.database.upper(),
        )

    def get_relationships_info_of_table(self, table: str) -> list[dict]:
        relationships = self.execute_query(self.query_relationship_information.format(table_name=table))
        relationship_info = []
        for relationship in relationships:
            column_name = relationship[8]
            ref_table_name = relationship[3]
            ref_column_name = relationship[4]
            relationship_info.append(
                {"column_name": column_name, "ref_table_name": ref_table_name, "ref_column_name": ref_column_name},
            )
        return relationship_info
