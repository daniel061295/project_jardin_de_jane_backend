class DynamoDBClientError(Exception):
    """Excepción personalizada para errores del cliente de DynamoDB."""
    def __init__(self, message: str = "Error en cliente de DynamoDB"):
        super().__init__(message)