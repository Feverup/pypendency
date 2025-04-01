from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition


def load(container_builder: ContainerBuilder):
    container_builder.set_definition(
        Definition('example.A', 'tests.resources.class_a.A')
    )

    x = 42
    x.append("This will cause an AttributeError")
