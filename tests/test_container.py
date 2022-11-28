from unittest import TestCase
from unittest.mock import sentinel

from pypendency import exceptions
from pypendency.argument import Argument
from pypendency.container import Container
from pypendency.definition import Definition
from tests.resources.class_a import A
from tests.resources.class_b import B
from tests.resources.class_c import C


class TestContainer(TestCase):
    def setUp(self) -> None:
        self.container = Container([])
        self.definition_a = Definition(
            "example.A",
            "tests.resources.class_a.A"
        )
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

    def test_is_resolved_is_false_on_instantiation(self):
        self.assertFalse(self.container.is_resolved())

    def test_is_resolved_is_true_after_getting_service_from_container(self):
        self.container.set("test_identifier1", self)
        self.container.get("test_identifier1")
        self.assertTrue(self.container.is_resolved())

    def test_set_cant_be_done_after_resolving_container(self):
        self.container.resolve()
        with self.assertRaises(exceptions.ForbiddenChangeOnResolvedContainer):
            self.container.set("test_identifier1", None)

    def test_set_can_be_done_after_resolving_container_when_test_mode(self):
        self.container.resolve()
        self.container.enable_test_mode()
        try:
            self.container.set("test_identifier1", None)
        except Exception as e:
            self.fail("set should not raise an exception for a resolved container in test mode")

    def test_set_cant_be_done_twice_for_the_same_identifier(self):
        self.container.set("test_identifier1", None)

        with self.assertRaises(exceptions.ServiceAlreadyDefined):
            self.container.set("test_identifier1", None)

    def test_set_sets_the_identifier_and_can_be_retrieved(self):
        self.container.set("test_identifier1", sentinel.service)
        self.assertIs(
            sentinel.service,
            self.container.get("test_identifier1"),
        )

    def test_get_fails_when_identifier_is_not_found(self):
        container = Container([
            self.definition_b
        ])

        with self.assertRaises(exceptions.ServiceNotFoundInContainer):
            container.get("example.B")

    def test_get_service_from_definitions(self):
        container = Container([
            self.definition_a,
            self.definition_c,
            self.definition_b,
        ])

        c = container.get("example.C")
        self.assertIsInstance(c, C)
        self.assertEqual("test_param", c.kw_arg)
        self.assertIsInstance(c.a, A)
        self.assertIsInstance(c.b, B)

    def test_get_with_invalid_fqn(self):
        container = Container([
            Definition(
                "example.A",
                "tests.resources.non_existing_path.class_a.A"
            ),
            self.definition_b,
        ])

        with self.assertRaises(exceptions.ServiceNotFoundFromFullyQualifiedName):
            container.get("example.B")

    def test_get_with_missing_parameters_for_instantiation(self):
        container = Container([
            Definition(
                "example.C",
                "tests.resources.class_c.C"
            ),
        ])

        with self.assertRaisesRegex(
            exceptions.ServiceInstantiationFailed,
            "Type tests.resources.class_c.C cannot be instantiated by the container"
        ):
            container.get("example.C")

    def test_get_with_more_parameters_than_expected(self):
        container = Container([
            Definition(
                "example.A",
                "tests.resources.class_a.A",
                [Argument("unexpected_argument", "test_param")],
            ),
            self.definition_b,
            self.definition_c
        ])

        with self.assertRaisesRegex(
            exceptions.ServiceInstantiationFailed,
            "Type tests.resources.class_a.A cannot be instantiated by the container"
        ):
            container.get("example.C")

    def test_has(self):
        container = Container([
            Definition("example", "example.fqn"),
        ])
        self.assertTrue(container.has("example"))
        self.assertFalse(container.has("other_example"))
