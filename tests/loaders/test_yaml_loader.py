import os
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
        self.current_dir = os.path.dirname(__file__)

    def test_load_fails_for_non_absolute_path(self):
        with self.assertRaises(exceptions.PathNotAbsolute):
            self.loader.load("relative/path")

    def test_load_fails_for_non_existing_yaml(self):
        with self.assertRaises(exceptions.ResourceNotFound):
            self.loader.load("/non/existing/path")

    def test_load_fails_for_invalid_yaml(self):
        path = os.path.join(self.current_dir, "..", "resources", "test_invalid_di.yaml")
        with self.assertRaises(exceptions.ParsingErrorOnResource):
            self.loader.load(path)

    def test_load_does_nothing_for_empty_yaml(self):
        mocked_container = Mock(spec=ContainerBuilder)
        path = os.path.join(self.current_dir, "..", "resources", "test_empty.yaml")
        YamlLoader(mocked_container).load(path)
        mocked_container.set_definition.assert_not_called()

    def test_load_works_as_expected(self):
        path = os.path.join(self.current_dir, "..", "resources", "test_di.yaml")
        self.loader.load(path)
        self.assertIsInstance(
            self._container_builder.get("example.C"),
            C
        )

    def test_load_dir(self):
        path = os.path.join(self.current_dir, "..", "resources", "loaders")
        self.loader.load_dir(path)
        self.assertIsInstance(self._container_builder.get("same_level_file"), A)
        self.assertIsInstance(self._container_builder.get("one_level_file"), A)
        self.assertIsInstance(self._container_builder.get("two_levels_file"), A)

        with self.assertRaises(ServiceNotFoundInContainer):
            self._container_builder.get("should_not_exist")

    def test_load_dir_fails_for_non_absolute_path(self):
        with self.assertRaises(exceptions.PathNotAbsolute):
            self.loader.load_dir("tests/resources/loaders")
