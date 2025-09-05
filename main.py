import logging
from fastapi import FastAPI
from mangum import Mangum
import colorlog

from controllers.product_controller import ProductController 
from core.global_container import GlobalContainer

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
handler = Mangum(app)

product_controller = ProductController(container=GlobalContainer.get_container())   
app.include_router(product_controller.get_router())
