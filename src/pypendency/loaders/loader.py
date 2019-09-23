from abc import ABC, abstractmethod


class Loader(ABC):
    @abstractmethod
    def load(self, resource: str) -> None: pass
