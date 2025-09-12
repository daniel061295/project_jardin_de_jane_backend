from models.base_dynamo_model import BaseDynamoModel

class ProductModel(BaseDynamoModel):
    name: str
    price: int
    image: str
    category: str
    subCategory: str