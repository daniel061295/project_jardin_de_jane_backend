from clients.dynamo_db_client import DynamoDBClient
from config.config import Config
from models.category_model import CategoryModel
from repositories.base_dynamo_repository import BaseDynamoRepository


class CategoryRepository(BaseDynamoRepository[CategoryModel]):
    def __init__(self, client:DynamoDBClient, config:Config):
        super().__init__(client=client, config=config, partition_key="id")
        