from models.base_dynamo_model import BaseDynamoModel

class SubcategoryModel(BaseDynamoModel):
    name: str
    description: str
