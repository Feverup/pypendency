import os
from abc import ABC, abstractmethod

from pypendency.loaders.exceptions import PathNotAbsolute


class Loader(ABC):
    @abstractmethod
    def load(self, resource: str) -> None: pass

    @abstractmethod
    def load_dir(self, directory: str) -> None: pass

    def _guard_path_is_absolute(self, path: str) -> None:
        if not os.path.isabs(path):
            raise PathNotAbsolute(path)
