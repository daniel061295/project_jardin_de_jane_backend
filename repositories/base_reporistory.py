import logging
from typing import Generic, TypeVar, Type, List, Optional
from pydantic import BaseModel

from clients.base_client import BaseClient
from config.config import Config

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, client: BaseClient, config: Config, partition_key: str = "id"):
        self.client = client
        self.config = config
        self.partition_key = partition_key  # clave primaria principal

    def create(self, entity: T) -> bool:
        return self.client.create(entity)

    def update(self, entity: T) -> bool:
        return self.client.update(entity)

    def find_by_id(self, entity_id: str) -> Optional[T]:
        return self.client.get({self.partition_key: entity_id})

    def delete(self, entity_id: str) -> bool:
        return self.client.delete({self.partition_key: entity_id})

    def list_all(self) -> List[T]:
        return self.client.get_all()

    def query(self, key_condition) -> List[T]:
        return self.client.query(key_condition)
    
