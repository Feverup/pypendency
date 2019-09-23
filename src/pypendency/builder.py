from typing import Optional, List

from pypendency import exceptions
from pypendency.definition import Definition
from pypendency.container import Container


class ContainerBuilder(Container):
    _instance: Optional["ContainerBuilder"] = None

    def __init__(self, definitions: List[Definition]):
        ContainerBuilder._instance = self
        super().__init__(definitions)

    @classmethod
    def get_container_instance(cls):
        if cls._instance is None:
            cls._instance = cls([])

        return cls._instance

    def set_definition(self, definition: Definition) -> None:
        if self.is_resolved():
            raise exceptions.ForbiddenChangeOnResolvedContainer()

        if self.has(definition.identifier):
            raise exceptions.ServiceAlreadyDefined(definition.identifier)

        self._service_mapping.update({
            definition.identifier: definition
        })


container_builder = ContainerBuilder.get_container_instance()
