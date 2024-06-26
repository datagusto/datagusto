from logging import getLogger
from typing import Any

import psycopg2

from .connection import Connection
from .types import PostgreSQLConfig

logger = getLogger("uvicorn.app")

TABLES_SQL = """
SELECT table_name FROM information_schema.tables
WHERE table_schema='{database_schema}'
    AND table_type='BASE TABLE'
    AND table_catalog='{database_name}'
"""

COLUMN_INFORMATION_SQL = """
SELECT * FROM information_schema.columns
WHERE table_schema = '{database_schema}'
    AND table_name   = '{table_name}'
    AND table_catalog='{database_name}'
"""

RELATIONSHIP_INFORMATION_SQL = """
SELECT
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
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


class PostgreSQLConnection(Connection):
    connection: Any = None
    cursor: Any = None
    schema: str = None

    def post_init(self):
        self.schema = self.config.pop("schema", "public")

    def validate_config(self) -> bool:
        # validate the config by initializing the MySQLConfig pydantic class
        try:
            PostgreSQLConfig(**self.config)
        except Exception:
            logger.exception("Invalid MySQL config: %s", self.config)
            return False
        return True

    def test_connection(self) -> bool:
        try:
            _connection = psycopg2.connect(**self.config)
            _connection.close()
        except psycopg2.DatabaseError:
            return False
        return True

    def set_cursor(self):
        if not self.connection:
            self.connection = psycopg2.connect(**self.config)
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
        self.cursor.execute(TABLES_SQL.format(database_name=self.get_database_name(), database_schema=self.schema))
        tables = self.cursor.fetchall()
        self.close()
        return [table[0] for table in tables]

    def get_all_columns(self):
        tables = self.get_all_tables()
        self.set_cursor()
        all_columns = {}
        for table in tables:
            logger.debug("Getting column information (metadata) of table :" + table)
            self.cursor.execute(COLUMN_INFORMATION_SQL.format(
                database_name=self.get_database_name(),
                database_schema=self.schema,
                table_name=table)
            )
            columns = self.cursor.fetchall()
            self.cursor.execute(RELATIONSHIP_INFORMATION_SQL.format(
                database_name=self.get_database_name(),
                database_schema=self.schema,
                table_name=table)
            )
            relationships = self.cursor.fetchall()

            for column in columns:
                (table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable,
                 data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_precision_radix,
                 numeric_scale, datetime_precision, interval_type, interval_precision, character_set_catalog,
                 character_set_schema, character_set_name, collation_catalog, collation_schema, collation_name,
                 domain_catalog, domain_schema, domain_name, udt_catalog, udt_schema, udt_name, scope_catalog,
                 scope_schema, scope_name, maximum_cardinality, dtd_identifier, is_self_referencing, is_identity,
                 identity_generation, identity_start, identity_increment, identity_maximum, identity_minimum,
                 identity_cycle, is_generated, generation_expression, is_updatable) = column
                column_info = {
                    "column_name": column_name,
                    "column_type": data_type,
                }

                # Using next() with a generator expression to find the first matching relationship or None
                _, ref_table_name, ref_column_name = next((r for r in relationships if column_name == r[0]),
                                                          (None, None, None))
                if ref_table_name:
                    column_info.update({
                        "referenced_table_name": ref_table_name,
                        "referenced_column_name": ref_column_name
                    })
                    relationships.remove((column_name, ref_table_name, ref_column_name))

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
        query = f"SELECT '{column}' FROM {table} LIMIT {limit}"
        return self.execute_query(query)

    def select_table(self, table: str, limit: int = 1000):
        query = f"SELECT * FROM {table} LIMIT {limit}"
        return self.execute_query(query)
