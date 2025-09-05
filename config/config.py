import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

class Config:
    """Clase de configuración con atributos dinámicos desde .env"""
    def __init__(self):
        pass

# Añadir dinámicamente los atributos de clase
for key, value in os.environ.items():
    setattr(Config, key, value)