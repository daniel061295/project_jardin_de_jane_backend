from abc import ABC
from typing import Callable, List
from fastapi import APIRouter

class BaseController(ABC):
    def __init__(self, container):
        self.container = container
        self.router = APIRouter()
    
    def get_router(self) -> APIRouter:
        return self.router

    def add_api_route(self, path: str, endpoint: Callable, methods: List[str]):
        """
        Registra la ruta con y sin slash final automáticamente.
        Ejemplo:
            path="/" -> /products y /products/
            path="/{id}" -> /products/{id} (no duplica)
        """
        # Si es ruta raíz ("" o "/") → registrar las dos variantes
        if path in ("", "/"):
            clean_path = ""
            self.router.add_api_route(clean_path, endpoint, methods=methods)
            self.router.add_api_route("/", endpoint, methods=methods)
        else:
            # Para rutas con parámetros u otras, solo una vez
            self.router.add_api_route(path, endpoint, methods=methods)
