from tests.resources.class_a import A
from tests.resources.class_b import B


class C:
    def __init__(self, a: A, b: B, kw_arg=None):
        self.a = a
        self.b = b
        self.kw_arg = kw_arg
