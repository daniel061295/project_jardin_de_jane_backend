from typing import List
from models.base_dynamo_model import BaseDynamoModel
from models.subcategory_model import SubcategoryModel

class CategoryModel(BaseDynamoModel):
    name: str
    icon: str
    description: str
    subcategories: List[SubcategoryModel] = []
