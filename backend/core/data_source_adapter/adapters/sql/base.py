from abc import ABC
from logging import getLogger
from typing import Union

from sqlalchemy import text

from ...config import SqlConfig, SqlFileServerConfig
from ..base import DataSourceBase

logger = getLogger()


class SqlBase(DataSourceBase, ABC):
    engine: any
    sql_config: Union[SqlConfig, SqlFileServerConfig]

    query_show_all_tables = "SHOW TABLES"
    query_column_information = ""
    query_relationship_information = ""

    def validate_config(self) -> bool:
        try:
            SqlConfig(**self.config)
        except Exception:
            return False
        return True

    def test_connection(self) -> bool:
        try:
            self.engine.connect()
        except Exception as e:
            logger.exception(e)
            return False
        return True

    def get_database_name(self) -> str:
        return self.sql_config.database

    def get_all_tables(self) -> list[str]:
        result = self.execute_query(self.query_show_all_tables)
        return [table[0] for table in result]

    def execute_query(self, query: str) -> list[tuple]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()

    def get_columns_of_table(self, table: str) -> list[dict]:
        query = self.query_column_information.format(table_name=table)
        columns = self.execute_query(query)
        column_info = []

        for column in columns:
            column_name, column_type, extra, comment = column
            _info = {
                "column_name": column_name,
                "column_type": column_type,
                "extra": extra,
                "comment": comment,
            }

            # Remove empty and None fields
            _info = {k: v for k, v in _info.items() if v not in [None, ""]}
            column_info.append(_info)

        return column_info

    def get_relationships_info_of_table(self, table: str) -> list[dict]:
        relationships = self.execute_query(self.query_relationship_information.format(table_name=table))
        relationship_info = []
        for relationship in relationships:
            column_name, ref_table_name, ref_column_name = relationship
            relationship_info.append(
                {"column_name": column_name, "ref_table_name": ref_table_name, "ref_column_name": ref_column_name},
            )
        return relationship_info

    def get_all_columns(self) -> dict:
        tables = self.get_all_tables()
        all_columns = {}
        for table in tables:
            logger.debug("Getting column information (metadata) of table :" + table)
            columns = self.get_columns_of_table(table)
            relationships = self.get_relationships_info_of_table(table)

            for column_info in columns:
                column_name = column_info["column_name"]
                # Using next() with a generator expression to find the first matching relationship or None
                # _, ref_table_name, ref_column_name = next(
                relationship = next((r for r in relationships if column_name == r["column_name"]), None)
                if relationship:
                    column_info.update(
                        {
                            "referenced_table_name": relationship["ref_table_name"],
                            "referenced_column_name": relationship["ref_column_name"],
                        },
                    )
                    del relationship

                all_columns.setdefault(table, []).append(column_info)
        return all_columns

    def select_column(self, table: str, column: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT '{column}' FROM {table} LIMIT {limit}"  # noqa: S608
        return self.execute_query(query)

    def select_table(self, table: str, limit: int = 1000) -> list[tuple]:
        query = f"SELECT * FROM {table} LIMIT {limit}"  # noqa: S608
        return self.execute_query(query)


class SqlFileServerBase(SqlBase, ABC):
    def validate_config(self) -> bool:
        try:
            SqlFileServerConfig(**self.config)
        except Exception:
            return False
        return True
