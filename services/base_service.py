from abc import ABC
import logging

from repositories.base_dynamo_repository import BaseDynamoRepository


class BaseService(ABC):
    def __init__(self, repository: BaseDynamoRepository):
        self.repository = repository
        self._log = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)

    async def __aenter__(self) -> "BaseService":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.repository.dispose()
 