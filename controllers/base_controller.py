from abc import ABC
from fastapi import APIRouter

class BaseController(ABC):
    def __init__(self, container):
        self.container = container
        self.router = APIRouter()
    
    def get_router(self) -> APIRouter:
        return self.router
