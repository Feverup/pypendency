import os
from abc import ABC, abstractmethod

from pypendency.loaders.exceptions import PathNotAbsolute


class Loader(ABC):
    @abstractmethod
    def load(self, resource: str) -> None: pass

    @abstractmethod
    def load_dir(self, directory: str) -> None: pass

    def guard_path_is_absolute(self, path: str):
        if not os.path.isabs(path):
            raise PathNotAbsolute(path)
