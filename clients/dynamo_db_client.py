from typing import List, Optional, Type, TypeVar
import boto3
import logging
from pydantic import BaseModel
from clients.base_client import BaseClient
from config.config import Config
from core.exceptions.dynamodb_client_exception import DynamoDBClientError

T = TypeVar("T", bound=BaseModel)

class DynamoDBClient(BaseClient[T]):
    def __init__(self, table_name: str, config: Config,  model: Type[T]) :
        super().__init__(table_name, config, model)
        self.dynamodb = boto3.resource("dynamodb", region_name=self.config.REGION)
        self.table = self.dynamodb.Table(self.table_name)

    def update(self, item: T) -> bool:
        """Inserta o reemplaza un item"""
        try:
            self.table.put_item(Item=item.model_dump(mode="json"))
            return True
        except DynamoDBClientError as e:
            logging.error(f"Error en put_item: {e}")
            return False

    def create(self, item: T) -> bool:
        """Crea un nuevo item"""
        try:
            self.table.put_item(Item=item.model_dump(mode="json"))
            return True
        except DynamoDBClientError as e:
            logging.error(f"Error en create: {e}")
            return False

    def get(self, key: dict) -> Optional[T]:
        """Obtiene un item por clave primaria"""
        try:
            response = self.table.get_item(Key=key)
            if "Item" in response:
                return self.model(**response["Item"])
            return None
        except DynamoDBClientError as e:
            logging.error(f"Error en get_item: {e}")
            return None

    def delete(self, key: dict) -> bool:
        """Elimina un item por clave primaria"""
        try:
            self.table.delete_item(Key=key)
            return True
        except DynamoDBClientError as e:
            logging.error(f"Error en delete_item: {e}")
            return False

    def get_all(self) -> List[T]:
        """Escanea todos los items de la tabla"""
        items: List[T] = []
        try:
            response = self.table.scan()
            items.extend([self.model(**i) for i in response.get("Items", [])])

            while "LastEvaluatedKey" in response:
                response = self.table.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                items.extend([self.model(**i) for i in response.get("Items", [])])

            return items
        except DynamoDBClientError as e:
            logging.error(f"Error en scan: {e}")
            return []

    def query(self, key_condition) -> List[T]:
        """Consulta usando KeyConditionExpression"""
        response = self.table.query(KeyConditionExpression=key_condition)
        return [self.model(**item) for item in response.get("Items", [])]

