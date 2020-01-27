from types import ModuleType

from pypendency.builder import ContainerBuilder


class PythonLoadableModuleType(ModuleType):
    def load(self, container_builder: ContainerBuilder) -> None: pass
