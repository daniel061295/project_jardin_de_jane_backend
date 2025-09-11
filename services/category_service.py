from models.category_model import CategoryModel
from repositories.category_repository import CategoryRepository
from services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository=repository)

    async def get_category(self, category_id: str) -> CategoryModel:
        return self.repository.find_by_id(category_id)

    async def list_categories(self) -> list[CategoryModel]:
        return self.repository.list_all()

    async def create_category(self, category_data: CategoryModel) -> bool:
        return self.repository.create(category_data)

    async def update_category(self, category_data: CategoryModel) -> bool:
        return self.repository.update(category_data)

    async def delete_category(self, category_id: str) -> bool:
        return self.repository.delete(category_id)