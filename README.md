# Pypendency
Pypendency is a dependency injection library for python 3.6+.

## Installation
```bash
pip install pypendency
```

## Usage
Pypendency supports:
* Declaration of explicit dependencies for each registered service.
* Lazy evaluation (dependencies are not evaluated and instantiated until they are required)
* Loading dependencies from different sources, such as python file, yaml file or directories. 
Also, it can be done programmatically.

#### Examples

```python
# application_bootstrap.py

from pypendency.builder import container_builder
from pypendency.definition import Definition
from pypendency.loaders.yaml_loader import YamlLoader
from pypendency.loaders.py_loader import PyLoader

# Manually
container_builder.set('random_object', object())
container_builder.set_definition(
    Definition('another_random_object', 'builtins.object')
)

# File by file
YamlLoader(container_builder).load('path_to_yaml/example_di.yaml')
PyLoader(container_builder).load('python.file.namespace.example_di')

# Specifying a directory
YamlLoader(container_builder).load_dir('path_to_yaml')
PyLoader(container_builder).load_dir('python/file/namespace/')
```

```yaml
# path_to_yaml/example_di.yaml

example_class_identifier:
    fqn: example.class.namespace.ClassName
    args:
        - '@another_example_class_identifier'
    kwargs:
        example_kwarg: '@random_object'
```

```python
# python/file/namespace/example_di.py

from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition


def load(container_builder: ContainerBuilder):
    container_builder.set("literal_string", "example_literal_string")
    container_builder.set_definition(
        Definition(
            "another_example_class_identifier",
            "another.example.class.namespace.AnotherClassName",
            [
                Argument.no_kw_argument("@literal_string"),
                Argument("kw_arg_example", "@literal_string"),
            ]
        )    
    )
```

## Running tests
Build the docker image:
```bash
docker build . -t pypendency-dev
```

Run tests:
```bash
docker run -v $(pwd)/.:/usr/src/app pypendency-dev bash -c "pipenv run make run-tests"
```
