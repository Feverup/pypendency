from typing import Optional, List

from pypendency.container import Container
from pypendency.definition import Definition


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


container_builder = ContainerBuilder.get_container_instance()
