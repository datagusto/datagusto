from abc import ABC, abstractmethod
from logging import getLogger

logger = getLogger("uvicorn.app")


class Connection(ABC):
    owner_id: int
    name: str
    description: str
    config: dict

    def __init__(self, owner_id: int, name: str, description: str, config: dict):
        self.owner_id = owner_id
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
