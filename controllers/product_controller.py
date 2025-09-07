from fastapi import HTTPException
from fastapi import status
from controllers.base_controller import BaseController
from core.dependency_injector import DependencyContainer
from models.product_model import ProductModel
from services.product_service import ProductService

class ProductController(BaseController):
    def __init__(self, container: DependencyContainer):
        super().__init__(container)
    
        self.router.prefix = "/products"
        self.router.add_api_route("/", self.list_items, methods=["GET"])
        self.router.add_api_route("/", self.create_item, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_item, methods=["PUT"])
        self.router.add_api_route("/{id}", self.get_item, methods=["GET"])
        self.router.add_api_route("/{id}", self.delete_item, methods=["DELETE"])

    async def list_items(self):
        try:
            service: ProductService = self.container.get_service(ProductService)
            items = await service.list_products()
            return {"items": items}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_item(self, id: str):
        service: ProductService = self.container.get_service(ProductService)
        try:
            item = await service.get_product(id)
            if not item:
                raise HTTPException(status_code=404, detail="Product not found")
            return {"item": item}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_item(self, item: dict):
        service: ProductService = self.container.get_service(ProductService)
        try:
            input_data = ProductModel(**item)
            await service.create_product(input_data)
            return {"item": input_data.model_dump()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_item(self, id: str, item: dict):
        service: ProductService = self.container.get_service(ProductService)
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parameter 'id' is required")
        try:
            updated_item = ProductModel(**item, id=id)
            await service.update_product(updated_item)
            return {"item": updated_item.model_dump()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_item(self, id: str):
        service: ProductService = self.container.get_service(ProductService)
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parameter 'id' is required")
        try:
            await service.delete_product(id)
            return {"message": "Product deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
