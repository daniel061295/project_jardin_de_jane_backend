from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel

from config.config import Config

T = TypeVar("T", bound=BaseModel)

class BaseClient(ABC, Generic[T]):
    def __init__(self, table_name: str, config: Config, model: Type[T]):
        self.table_name = table_name
        self.config = config
        self.model = model

    @abstractmethod
    def create(self, item: T) -> bool:
        pass

    @abstractmethod
    def update(self, item: T) -> bool:
        pass

    @abstractmethod
    def get(self, key: dict) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, key: dict) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def query(self, key_condition) -> List[T]:
        pass