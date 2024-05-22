from abc import ABC, abstractmethod
from logging import getLogger

logger = getLogger("uvicorn.app")


class Connection(ABC):
    name: str
    description: str
    config: dict

    def __init__(self, name: str, description: str, config: dict):
        self.name = name
        self.description = description
        self.config = config
        valid = self.validate_config()
        if not valid:
            raise ValueError("Invalid config data.")

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
