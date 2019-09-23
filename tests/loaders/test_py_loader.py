from unittest import TestCase

from pypendency.builder import ContainerBuilder
from pypendency.loaders import exceptions
from pypendency.loaders.py_loader import PyLoader
from tests.resources.class_a import A
from tests.resources.class_b import B
from tests.resources.class_c import C


class TestPyLoader(TestCase):
    def setUp(self) -> None:
        self._container_builder = ContainerBuilder([])
        self.loader = PyLoader(self._container_builder)

    def test_load_fails_for_non_existing_file(self):
        with self.assertRaises(exceptions.ResourceNotFound):
            self.loader.load("nonexistingpath")

    def test_load_fails_for_loader_without_load_method(self):
        with self.assertRaises(exceptions.MissingLoaderMethod):
            self.loader.load("tests.resources.test_di_no_load_method")

    def test_load_works_as_expected(self):
        self.loader.load("tests.resources.test_di")
        c = self._container_builder.get("example.C")
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.b, B)
        self.assertIsInstance(c.a, A)
