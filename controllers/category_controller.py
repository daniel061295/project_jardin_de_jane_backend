import logging
from fastapi import HTTPException
from fastapi import status
from controllers.base_controller import BaseController
from core.dependency_injector import DependencyContainer
from models.category_model import CategoryModel
from services.category_service import CategoryService

class CategoryController(BaseController):
    def __init__(self, container: DependencyContainer):
        super().__init__(container)
    
        self.router.prefix = "/categories"
        self.router.add_api_route("/", self.list_items, methods=["GET"])
        self.router.add_api_route("/", self.create_item, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_item, methods=["PUT"])
        self.router.add_api_route("/{id}", self.get_item, methods=["GET"])
        self.router.add_api_route("/{id}", self.delete_item, methods=["DELETE"])

    async def list_items(self):
        try:
            service: CategoryService = self.container.get_service(CategoryService)
            items = await service.list_categories()
            return {"items": items}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_item(self, id: str):
        service: CategoryService = self.container.get_service(CategoryService)
        try:
            item = await service.get_category(id)
            if not item:
                raise HTTPException(status_code=404, detail="Category not found")
            return {"item": item}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_item(self, item: dict):
        service: CategoryService = self.container.get_service(CategoryService)
        try:
            input_data = CategoryModel(**item)
            logging.info(f"Creating category with data: {input_data}")
            await service.create_category(input_data)
            return {"item": input_data.model_dump()}
        except Exception as e:
            logging.error(f"Error creating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def update_item(self, id: str, item: dict):
        service: CategoryService = self.container.get_service(CategoryService)
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parameter 'id' is required")
        try:
            updated_item = CategoryModel(**item, id=id)
            await service.update_category(updated_item)
            return {"item": updated_item.model_dump()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_item(self, id: str):
        service: CategoryService = self.container.get_service(CategoryService)
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parameter 'id' is required")
        try:
            await service.delete_category(id)
            return {"message": "Category deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
