import logging
from fastapi import FastAPI
from mangum import Mangum
import colorlog
from fastapi.middleware.cors import CORSMiddleware
from controllers.category_controller import CategoryController
from controllers.product_controller import ProductController 
from core.global_container import GlobalContainer
from registres import dependency_registry  # Asegura que las dependencias estén registradas

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'blue',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logging.basicConfig(level=logging.INFO, handlers=[handler])

app = FastAPI()
# ⚠️ Acepta cualquier origen (para pruebas o desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # todos los métodos
    allow_headers=["*"],  # todas las cabeceras
)
handler = Mangum(app)

product_controller = ProductController(container=GlobalContainer.get_container())
category_controller = CategoryController(container=GlobalContainer.get_container())
  
app.include_router(product_controller.get_router())
app.include_router(category_controller.get_router())
