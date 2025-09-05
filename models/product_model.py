from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    price: int
    image: str
    category: str
    subCategory: str

    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        }
    }