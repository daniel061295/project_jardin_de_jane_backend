from clients.dynamo_db_client import DynamoDBClient
from config.config import Config
from core.global_container import GlobalContainer
from models.category_model import CategoryModel
from models.product_model import ProductModel
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from services.category_service import CategoryService
from services.product_service import ProductService

# Registrar dependencias
container = GlobalContainer.get_container()
container.add_singleton(Config, lambda: Config())

# Registro de Repositorios
container.add_transient(
    ProductRepository,
    lambda: ProductRepository(
        client=DynamoDBClient(
            table_name=container.get_service(Config).PRODUCTS_TABLE,
            config=container.get_service(Config),
            model=ProductModel
        ),
        config=container.get_service(Config)
    )
)
container.add_transient(
    CategoryRepository,
    lambda: CategoryRepository(
        client=DynamoDBClient(
            table_name=container.get_service(Config).CATEGORIES_TABLE,
            config=container.get_service(Config),
            model=CategoryModel
        ),
        config=container.get_service(Config)
    )
)

# Registro de Servicios
container.add_transient(ProductService)
container.add_transient(CategoryService)
