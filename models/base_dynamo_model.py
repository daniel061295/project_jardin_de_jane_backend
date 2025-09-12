from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BaseDynamoModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)

    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        }
    }