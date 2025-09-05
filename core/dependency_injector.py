import asyncio
import enum
import inspect
from typing import Any, Callable, Dict, Optional, Type
import typing
from core.disaposable import IDisposable
from core.exceptions.not_found_error import NotFoundError
from core.exceptions.validation_error import ValidationError

class ServiceLifetime(enum.Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"

class ServiceRegistration:
    """Registro de servicios para la inyección de dependencias."""
    def __init__(self, factory: Callable[[], Any], lifetime: ServiceLifetime):
        self.factory = factory
        self.lifetime = lifetime

class DependencyContainer:
    """Contenedor de dependencias."""
    def __init__(self):
        self._services: Dict[str, ServiceRegistration] = {}
        self._singletons: Dict[str, Any] = {}

    def add_singleton(self, service_type: Type, implementation_factory: Optional[Callable[[], Any]] = None):
        """Registra un servicio como singleton."""
        self.add_service(
            service_type, 
            implementation_factory or (lambda: self._create_instance(service_type)), 
            ServiceLifetime.SINGLETON)

    def add_transient(self, service_type: Type, implementation_factory: Optional[Callable[[], Any]] = None):
        """Registra un servicio como transient."""
        self.add_service(
            service_type, 
            implementation_factory or (lambda: self._create_instance(service_type)), 
            ServiceLifetime.TRANSIENT)

    def add_service(self, service_type: Type, implementation_factory: Callable[[], Any], lifetime: ServiceLifetime):
        """Registra un servicio en el contenedor de dependencias."""
        if service_type not in self._services:
            self._services[service_type] = []

        self._services[service_type].append(ServiceRegistration(factory=implementation_factory, lifetime=lifetime))

    def _get_service(self, service_type: Type, scope: Optional[Dict[Type, Any]] = None) -> Any:
        """Obtiene una instancia de un servicio del contenedor de dependencias."""
        services = self._services.get(service_type, [])
        if not services or len(services) == 0:
            raise NotFoundError(f"No se ha registrado el servicio para {service_type.__name__}")

        if len(services) == 1:
            return self._resolve_service(services[0], service_type, scope)

        return [self._resolve_service(reg, service_type, scope) for reg in services]

    def _resolve_service(self, registration: ServiceRegistration, service_type: Type, scope: Optional[Dict[Type, Any]] = None) -> Any:
        """Resuelve una instancia de un servicio segun su ciclo de vida"""
        lifeTime = registration.lifetime
        factory = registration.factory

        if lifeTime == ServiceLifetime.SINGLETON:
            if service_type not in self._singletons:
                self._singletons[service_type] = factory()
            return self._singletons[service_type]

        elif lifeTime == ServiceLifetime.TRANSIENT:
            return factory()

        else:
            raise ValidationError(f"Tipo de ciclo de vida no soportado: {lifeTime}")
        
    def _create_instance(self, cls: Type) -> Any:
        """ 
        Crea una instancia de la clase 'cls' inyectando automaticamente sus
        dependencias en el constructor.
        """
        ctor = getattr(cls,"__init__")
        sig = inspect.signature(ctor)
        params = list(sig.parameters.values())[1:]
        
        args = []
        for p in params: 
            if p.annotation == inspect._empty:
                raise ValidationError(f"El parametro '{p.name}' del constructor de '{cls.__name__}' no tiene una anotación de tipo.")

            origin = typing.get_origin(p.annotation)
            if origin is list:
                item_type = typing.get_args(p.annotation)[0]
                dependency = self._get_service(item_type)
                
                if not isinstance(dependency, list):
                    dependency = [dependency]
                    
                args.append(dependency)
            
            else:
                dependency = self._get_service(p.annotation)
                args.append(dependency)

        return cls(*args)

    async def shutdown(self):
        """Realiza la limpieza de los servicios."""
        for instance in self._singletons.values():
            if isinstance(instance, IDisposable):
                if hasattr(instance, "dispose") and callable(instance.dispose):
                    if asyncio.iscoroutinefunction(instance.dispose):
                        await instance.dispose()
                    else:
                        instance.dispose()
