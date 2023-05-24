from unittest import TestCase

from pypendency.argument import Argument


class TestDefinition(TestCase):
    def test_argument_without_keywords(self):
        self.assertEqual(Argument(None, "value"), Argument.no_kw_argument("value"))
