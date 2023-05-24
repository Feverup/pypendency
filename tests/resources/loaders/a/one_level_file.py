from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition


def load(container_builder: ContainerBuilder):
    container_builder.set_definition(Definition("one_level_file", "tests.resources.class_a.A"))
