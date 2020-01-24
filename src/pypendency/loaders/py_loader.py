import glob
from importlib.util import spec_from_file_location, module_from_spec
from pydoc import locate

from pypendency.builder import ContainerBuilder
from pypendency.loaders import exceptions
from pypendency.loaders.loader import Loader
from pypendency.types.python_loadable_module import PythonLoadableModuleType


class PyLoader(Loader):
    DEFAULT_TEMPORAL_LOAD_MODULE_NAME = "pypendency.loaders.py_loader.__tmp_imported_module"

    def __init__(self, container_builder: ContainerBuilder):
        self.__container_builder = container_builder

    def load(self, resource: str) -> None:
        self._guard_path_is_absolute(resource)
        self.__load_by_absolute_path(resource)

    def __load_by_absolute_path(self, resource: str) -> None:
        spec = spec_from_file_location(self.DEFAULT_TEMPORAL_LOAD_MODULE_NAME, resource)

        if spec is None or spec.loader is None:
            raise exceptions.ResourceNotFound(resource)

        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        self.__load_module(resource, module)

    def __load_module(self, resource: str, module: PythonLoadableModuleType) -> None:
        try:
            module.load(self.__container_builder)
        except AttributeError as e:
            raise exceptions.MissingLoaderMethod(resource) from e

    def load_by_module_name(self, resource: str) -> None:
        package = locate(resource)

        if package is None:
            raise exceptions.ResourceNotFound(resource)

        self.__load_module(resource, package)

    def load_dir(self, directory: str) -> None:
        self._guard_path_is_absolute(directory)
        for file in glob.glob(f"{directory}/**/[!_]*.py", recursive=True):
            self.__load_by_absolute_path(file)
