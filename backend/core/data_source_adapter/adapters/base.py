from abc import ABC, abstractmethod
from logging import getLogger

logger = getLogger("uvicorn.app")


class DataSourceBase(ABC):
    name: str
    description: str
    config: dict

    def __init__(self, name: str, description: str, config: dict) -> None:
        self.name = name
        self.description = description
        self.config = config
        valid = self.validate_config()
        if not valid:
            raise ValueError("Invalid config data.")
        self.post_init()

    @abstractmethod
    def post_init(self) -> None:
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def test_connection(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_database_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_all_tables(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_all_columns(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def select_table(self, table: str, limit: int = 1000) -> list[tuple]:
        raise NotImplementedError

    @abstractmethod
    def select_column(self, table: str, column: str, limit: int = 1000) -> list[tuple]:
        raise NotImplementedError
