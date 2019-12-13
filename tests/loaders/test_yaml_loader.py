from unittest import TestCase
from unittest.mock import Mock

from pypendency.builder import ContainerBuilder
from pypendency.exceptions import ServiceNotFoundInContainer
from pypendency.loaders import exceptions
from pypendency.loaders.yaml_loader import YamlLoader
from tests.resources.class_a import A
from tests.resources.class_c import C


class TestYamlLoader(TestCase):
    def setUp(self) -> None:
        self._container_builder = ContainerBuilder([])
        self.loader = YamlLoader(self._container_builder)

    def test_load_fails_for_non_existing_yaml(self):
        with self.assertRaises(exceptions.ResourceNotFound):
            self.loader.load("nonexistingpath")

    def test_load_fails_for_invalid_yaml(self):
        with self.assertRaises(exceptions.ParsingErrorOnResource):
            self.loader.load("tests/resources/test_invalid_di.yaml")

    def test_load_does_nothing_for_empty_yaml(self):
        mocked_container = Mock(spec=ContainerBuilder)
        YamlLoader(mocked_container).load("tests/resources/test_empty.yaml")
        mocked_container.set_definition.assert_not_called()

    def test_load_works_as_expected(self):
        self.loader.load("tests/resources/test_di.yaml")
        self.assertIsInstance(
            self._container_builder.get("example.C"),
            C
        )

    def test_load_dir(self):
        self.loader.load_dir("tests/resources/loaders")
        self.assertIsInstance(self._container_builder.get("same_level_file"), A)
        self.assertIsInstance(self._container_builder.get("one_level_file"), A)
        self.assertIsInstance(self._container_builder.get("two_levels_file"), A)

        with self.assertRaises(ServiceNotFoundInContainer):
            self._container_builder.get("should_not_exists")


