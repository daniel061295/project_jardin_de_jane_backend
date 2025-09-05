
from abc import ABC, abstractmethod


class IDisposable(ABC):
    @abstractmethod
    def dispose(self) -> None:
        pass