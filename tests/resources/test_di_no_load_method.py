from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


container_builder.set_definition(
    Definition('example.A', 'tests.resources.class_a.A')
)
container_builder.set_definition(
    Definition(
        'example.B',
        'tests.resources.class_b.B',
        [Argument.no_kw_argument("@example.A")]
    )
)
container_builder.set_definition(
    Definition(
        'example.C',
        'tests.resources.class_c.C',
        [
            Argument.no_kw_argument("@example.A"),
            Argument("b", "@example.B"),
            Argument("kw_arg", "test_param"),
        ]
    )
)
