class NotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra un servicio."""
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message)