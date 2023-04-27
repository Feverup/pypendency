from dataclasses import FrozenInstanceError
from unittest import TestCase

from pypendency.argument import Argument
from pypendency.definition import Definition


class TestDefinition(TestCase):
    def test_no_arguments_initialization(self):
        self.assertEqual(
            Definition("example1", "example2"),
            Definition("example1", "example2", []),
        )

    def test_definition_is_frozen(self):
        definition = Definition("example1", "example2")
        with self.assertRaises(FrozenInstanceError):
            definition.identifier = "Im going to fail :)"

    def test_definition_supports_adding_arguments(self):
        definition = Definition("example1", "example2")
        definition.arguments.append(Argument.no_kw_argument("example1"))
        self.assertEqual(1, len(definition.arguments))
