import os
import shutil
from logging import getLogger
from typing import Optional

import pandas as pd

from ..config import FileConfig
from .base import DataSourceBase

logger = getLogger("uvicorn.app")


FILE_STORAGE_PATH = os.path.join(".", "data", "files")


class FileDataSource(DataSourceBase):
    file_type: str

    def post_init(self):
        self.file_type = self.config.get("file_type")

    def validate_config(self) -> bool:
        # validate the config by initializing the MySQLConfig pydantic class
        try:
            FileConfig(**self.config)
        except Exception:
            logger.exception("Invalid MySQL config: %s", self.config)
            return False
        return True

    def test_connection(self) -> bool:
        try:
            self.read_file()
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.exception(e)
            return False
        return True

    def get_database_name(self) -> str:
        return "file"

    def get_all_tables(self) -> list:
        return ["file"]

    def get_all_columns(self) -> dict:
        df = self.read_file()
        all_columns = {"table": []}
        for column in df.columns:
            column_info = {
                "column_name": column,
                "column_type": str(df[column].dtype),
                "extra": "",
                "comment": "",
            }
            all_columns["table"].append(column_info)

        return all_columns

    def save_file(self, file):
        destination = self.get_path()
        try:
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file, buffer)
        finally:
            file.close()

    def select_column(self, table: str, column: str, limit: int = 1000):
        df = self.read_file(limit)
        if column not in df.columns:
            return []
        return df[column].tolist()

    def select_table(self, table: str, limit: int = 1000) -> list[tuple]:
        df = self.read_file(limit)
        data = [tuple(row) for row in df.itertuples(index=False, name=None)]
        return data

    def read_file(self, limit: int = 2) -> Optional[pd.DataFrame]:
        df = None
        if self.file_type == "csv":
            df = pd.read_csv(self.get_path(), nrows=limit)

        return df

    def get_path(self) -> str:
        saved_name = self.config.get("saved_name")
        return os.path.join(FILE_STORAGE_PATH, saved_name)
