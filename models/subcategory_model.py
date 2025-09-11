from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class SubcategoryModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    description: str
    
    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        }
    }