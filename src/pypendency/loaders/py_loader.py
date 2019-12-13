import glob
from pydoc import locate

from pypendency.builder import ContainerBuilder
from pypendency.loaders import exceptions
from pypendency.loaders.loader import Loader


class PyLoader(Loader):
    def __init__(self, container_builder: ContainerBuilder):
        self.__container_builder = container_builder

    def load(self, resource: str) -> None:
        package = locate(resource)

        if package is None:
            raise exceptions.ResourceNotFound(resource)

        try:
            package.load(self.__container_builder)
        except AttributeError as e:
            raise exceptions.MissingLoaderMethod(resource) from e

    def load_dir(self, directory: str) -> None:
        for file in glob.glob(f"{directory}/**/[!_]*.py", recursive=True):
            self.load(file[:-3].replace("/", "."))
