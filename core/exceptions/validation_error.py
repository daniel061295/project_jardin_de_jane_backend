class ValidationError(Exception):
    """Excepción lanzada cuando hay un error de validación."""
    def __init__(self, message: str = "Error de validación"):
        super().__init__(message)