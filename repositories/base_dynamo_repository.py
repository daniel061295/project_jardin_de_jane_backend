from typing import Optional, TypeVar

from pydantic import BaseModel

from clients.dynamo_db_client import DynamoDBClient
from config.config import Config
from repositories.base_reporistory import BaseRepository

T = TypeVar("T", bound=BaseModel)
class BaseDynamoRepository(BaseRepository[T]):
    def __init__(self, client: DynamoDBClient, config: Config, partition_key: str = "id", sort_key: Optional[str] = None):
        super().__init__(client, config, partition_key)
        self.sort_key = sort_key  # clave de ordenamiento secundaria, si aplica 

    def find_by_id(self, entity_id: str, sort_key_value: Optional[str] = None) -> Optional[T]:
        if sort_key_value:
            return self.client.get({self.partition_key: entity_id, self.sort_key: sort_key_value})
        return self.client.get({self.partition_key: entity_id})

    def delete(self, entity_id: str, sort_key_value: Optional[str] = None) -> bool:
        if sort_key_value:
            return self.client.delete({self.partition_key: entity_id, self.sort_key: sort_key_value})
        return self.client.delete({self.partition_key: entity_id})