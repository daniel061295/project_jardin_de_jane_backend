from typing import Optional
from clients.dynamo_db_client import DynamoDBClient
from config.config import Config
from repositories.base_dynamo_repository import BaseDynamoRepository
from models.product_model import ProductModel


class ProductRepository(BaseDynamoRepository[ProductModel]):
    def __init__(self, client:DynamoDBClient, config:Config):
        super().__init__(client=client, config=config, partition_key="id")

