from unittest import TestCase
from unittest.mock import sentinel

from pypendency import exceptions
from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition
from pypendency.tag import Tag
from tests.resources.class_c import C


class TestContainerBuilder(TestCase):
    def setUp(self) -> None:
        self.container_builder = ContainerBuilder([])
        self.definition_a = Definition("example.A", "tests.resources.class_a.A")
        self.definition_b = Definition(
            "example.B",
            "tests.resources.class_b.B",
            [Argument.no_kw_argument("@example.A")],
        )
        self.definition_c = Definition(
            "example.C",
            "tests.resources.class_c.C",
            [
                Argument.no_kw_argument("@example.A"),
                Argument("kw_arg", "test_param"),
                Argument("b", "@example.B"),
            ],
        )
        self.definition_d = Definition(
            "example.D",
            "tests.resources.class_c.C",
            [
                Argument.no_kw_argument("@example.A"),
                Argument("kw_arg", "test_param"),
                Argument("b", "@example.B"),
            ],
            {
                Tag(identifier="test_tag_A", value=sentinel.test_tag_A_value),
            },
        )
        self.definition_e = Definition(
            "example.E",
            "tests.resources.class_a.A",
            tags={
                Tag(identifier="test_tag_A", value=sentinel.test_tag_A_value),
                Tag(identifier="test_tag_B", value=sentinel.test_tag_B_value),
            },
        )

    def test_get_container_instance_retrieves_the_same_object(self):
        self.assertIs(ContainerBuilder.get_container_instance(), ContainerBuilder.get_container_instance())

    def test_set_definition_fails_if_resolved(self):
        self.container_builder.resolve()

        with self.assertRaises(exceptions.ForbiddenChangeOnResolvedContainer):
            self.container_builder.set_definition(self.definition_a)

    def test_set_definitions_sets_properly_so_services_can_be_retrieved(self):
        self.container_builder.set_definition(self.definition_b)
        self.container_builder.set_definition(self.definition_a)
        self.container_builder.set_definition(self.definition_c)
        self.container_builder.set_definition(self.definition_d)
        self.container_builder.set_definition(self.definition_e)
        self.assertIsInstance(self.container_builder.get("example.C"), C)
