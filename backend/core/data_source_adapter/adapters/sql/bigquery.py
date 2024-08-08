from logging import getLogger

from sqlalchemy import create_engine

from ...config import BigQueryConfig
from .base import SqlBase

logger = getLogger()

TABLES_SQL = """
SELECT table_name FROM {database_name}.INFORMATION_SCHEMA.TABLES
"""

COLUMN_INFORMATION_SQL = """
SELECT 
  column_name,
  data_type AS column_type,
  '' AS extra,
  '' AS comment
FROM 
  `{dataset_name}`.INFORMATION_SCHEMA.COLUMNS
WHERE 
  table_name = '{table_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
"""


class BigQueryAdapter(SqlBase):
    sql_config: BigQueryConfig

    def validate_config(self) -> bool:
        try:
            BigQueryConfig(**self.config)
        except Exception:
            return False
        return True

    def post_init(self) -> None:
        self.sql_config = BigQueryConfig(**self.config)
        self.engine = create_engine(
            self.sql_config.uri,
            credentials_info=self.sql_config.credentials,
        )
        self.query_show_all_tables = TABLES_SQL.format(
            database_name=self.sql_config.database,
        )
        self.query_column_information = COLUMN_INFORMATION_SQL.format(
            dataset_name=self.sql_config.dataset,
            table_name="{table_name}",
        )
