from unittest import TestCase

from pypendency.builder import ContainerBuilder

class TestContainerBuilder(TestCase):
    def setUp(self) -> None:
        self.container_builder = ContainerBuilder([])

    def test_get_container_instance_retrieves_the_same_object(self):
        self.assertIs(
            ContainerBuilder.get_container_instance(),
            ContainerBuilder.get_container_instance()
        )
