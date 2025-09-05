from core.dependency_injector import DependencyContainer

class GlobalContainer:
    _container: DependencyContainer = None

    @classmethod
    def get_container(cls) -> DependencyContainer:
        if cls._container is None:
            cls._container = DependencyContainer()
        return cls._container

    @classmethod
    def reset(cls):
        cls._container = None