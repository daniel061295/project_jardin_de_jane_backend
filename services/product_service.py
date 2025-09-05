from typing import List, Optional
from models.product_model import ProductModel
from repositories.product_repository import ProductRepository
from services.base_service import BaseService


class ProductService(BaseService):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

    async def create_product(self, product_data: ProductModel) -> bool:
        return self.repository.create(product_data)

    async def get_product(self, product_id: str) -> Optional[ProductModel]:
        return self.repository.find_by_id(product_id)

    async def update_product(self, product_data: ProductModel) -> bool:
        return self.repository.update(product_data)

    async def delete_product(self, product_id: str) -> bool:
        return self.repository.delete(product_id)

    async def list_products(self) -> List[ProductModel]:
        return self.repository.list_all()
