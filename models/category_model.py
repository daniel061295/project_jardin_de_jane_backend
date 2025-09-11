from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from models.subcategory_model import SubcategoryModel

class CategoryModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    icon: str
    description: str
    subcategories: List[SubcategoryModel] = []

    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        }
    }