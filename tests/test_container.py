from unittest import TestCase
from unittest.mock import sentinel, Mock

from pypendency import exceptions
from pypendency.argument import Argument
from pypendency.container import Container
from pypendency.definition import Definition
from pypendency.tag import Tag
from tests.resources.class_a import A
from tests.resources.class_b import B
from tests.resources.class_c import C


class TestContainer(TestCase):
    def setUp(self) -> None:
        self.container = Container([])
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
            "tests.resources.class_a.A",
            tags={
                Tag(identifier="test_tag_A", value=sentinel.test_tag_A),
                Tag(identifier="test_tag_B", value=sentinel.test_tag_B),
            },
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

    def test_set_sets_the_identifier_with_tags(self):
        self.container.set(
            "test_identifier1", sentinel.service, {Tag(identifier="test_tag_A", value=sentinel.tag_value)}
        )
        self.assertIs(
            sentinel.service,
            self.container.get("test_identifier1"),
        )
        self.assertIs(sentinel.service, self.container.get_by_tag_name("test_tag_A", sentinel.tag_value).pop())

    def test_get_fails_when_identifier_is_not_found(self):
        container = Container([self.definition_b])

        with self.assertRaises(exceptions.ServiceNotFoundInContainer):
            container.get("example.B")

    def test_get_service_from_definitions(self):
        container = Container(
            [
                self.definition_a,
                self.definition_c,
                self.definition_b,
                self.definition_d,
            ]
        )

        c = container.get("example.C")
        self.assertIsInstance(c, C)
        self.assertEqual("test_param", c.kw_arg)
        self.assertIsInstance(c.a, A)
        self.assertIsInstance(c.b, B)

    def test_get_with_invalid_fqn(self):
        container = Container(
            [
                Definition("example.A", "tests.resources.non_existing_path.class_a.A"),
                self.definition_b,
            ]
        )

        with self.assertRaises(exceptions.ServiceNotFoundFromFullyQualifiedName):
            container.get("example.B")

    def test_get_with_missing_parameters_for_instantiation(self):
        container = Container(
            [
                Definition("example.C", "tests.resources.class_c.C"),
            ]
        )

        with self.assertRaisesRegex(
            exceptions.ServiceInstantiationFailed,
            "Type tests.resources.class_c.C cannot be instantiated by the container",
        ):
            container.get("example.C")

    def test_get_with_more_parameters_than_expected(self):
        container = Container(
            [
                Definition(
                    "example.A",
                    "tests.resources.class_a.A",
                    [Argument("unexpected_argument", "test_param")],
                ),
                self.definition_b,
                self.definition_c,
            ]
        )

        with self.assertRaisesRegex(
            exceptions.ServiceInstantiationFailed,
            "Type tests.resources.class_a.A cannot be instantiated by the container",
        ):
            container.get("example.C")

    def test_get_by_tag_fails_when_tag_is_not_found(self):
        container = Container([self.definition_d])

        with self.assertRaises(exceptions.TagNotFoundInContainer):
            container.get_by_tag(Tag(identifier="test_tag_C", value=sentinel.test_unexisting_tag_value))

    def test_get_by_tag(self):
        container = Container(
            [
                self.definition_d,
                Definition(
                    "example.E",
                    "tests.resources.class_a.A",
                    tags={
                        Tag(identifier="test_tag_A", value=sentinel.test_tag_value),
                    },
                ),
            ]
        )

        services = container.get_by_tag(Tag(identifier="test_tag_A", value=sentinel.test_tag_value))

        self.assertEqual(1, len(services))
        self.assertIsInstance(services.pop(), A)

    def test_get_by_tag_name(self):
        container = Container(
            [
                self.definition_d,
                Definition(
                    "example.E",
                    "tests.resources.class_a.A",
                    tags={
                        Tag(identifier="test_tag_A", value=sentinel.test_tag_value),
                    },
                ),
            ]
        )

        services = container.get_by_tag_name("test_tag_A")

        self.assertEqual(2, len(services))
        self.assertIsInstance(services.pop(), A)
        self.assertIsInstance(services.pop(), A)

    def test_get_service_tags(self):
        container = Container([])
        test_service = object()
        test_tag = Tag(identifier="test_tag_A", value=sentinel.value)
        container.set("test_service", test_service, {test_tag})

        tags = container.get_service_tags("test_service")

        self.assertEqual(1, len(tags))
        self.assertEqual(list(tags)[0], test_tag)

    def test_has(self):
        container = Container(
            [
                Definition("example", "example.fqn"),
            ]
        )
        self.assertTrue(container.has("example"))
        self.assertFalse(container.has("other_example"))

    def test_add_resolved_callback(self):
        container = Container([])
        func_one = Mock()
        container.add_on_resolved_callback(func_one)
        self.assertEqual(1, len(container._on_resolved_callbacks))

        container.add_on_resolved_callback(func_one)
        self.assertEqual(1, len(container._on_resolved_callbacks))
        func_two = Mock()
        func_three = Mock()
        container.add_on_resolved_callback(func_two)
        container.add_on_resolved_callback(func_three)

        self.assertEqual(3, len(container._on_resolved_callbacks))

    def test_perform_on_resolved_callbacks(self):
        container = Container([])

        func_one = Mock()
        func_two = Mock()
        func_three = Mock()

        container.add_on_resolved_callback(func_one)
        container.add_on_resolved_callback(func_two)
        container.add_on_resolved_callback(func_three)

        container.resolve()

        func_one.assert_called_once()
        func_two.assert_called_once()
        func_three.assert_called_once()

    def test_perform_on_resolved_callbacks_exception(self):
        container = Container([])

        func_one = Mock()
        func_one.side_effect = Exception()
        container.add_on_resolved_callback(func_one)

        with self.assertRaises(exceptions.PypendencyCallbackException):
            container.resolve()

    def test_set_dependency_on_resolved_callback(self):
        container = Container([])

        def func_one() -> None:
            container.set("fqn", 1)

        container.add_on_resolved_callback(func_one)

        with self.assertRaises(exceptions.PypendencyCallbackException):
            container.resolve()

    def test_get_services_identifiers_by_tag_name(self):
        container = Container(
            [
                self.definition_d,
                Definition(
                    "example.E",
                    "tests.resources.class_a.A",
                    tags={
                        Tag(identifier="test_tag_A", value=sentinel.test_tag_A),
                    },
                ),
            ]
        )

        scenarios = [
            {
                "msg": "Without value",
                "tag_identifier": "test_tag_A",
                "tag_value": Tag.UNSET_VALUE,
            },
            {
                "msg": "With value",
                "tag_identifier": "test_tag_A",
                "tag_value": sentinel.test_tag_A,
            },
        ]

        for scenario in scenarios:
            with self.subTest(msg=scenario["msg"]):
                identifiers = container.get_services_identifiers_by_tag_name(
                    scenario["tag_identifier"], scenario["tag_value"]
                )

                self.assertEqual({"example.D", "example.E"}, identifiers)

    def test_get_services_identifiers_by_tag_name_raises_when_tag_doesnt_exist(self):
        container = Container(
            [
                self.definition_d,
                Definition(
                    "example.E",
                    "tests.resources.class_a.A",
                    tags={
                        Tag(identifier="test_tag_A", value=sentinel.test_tag_A),
                    },
                ),
            ]
        )

        with self.assertRaises(exceptions.TagNotFoundInContainer):
            container.get_services_identifiers_by_tag_name("this_tag_shouldn't_exist", None)
