import glob

import yaml

from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition
from pypendency.loaders import exceptions
from pypendency.loaders.loader import Loader


class YamlLoader(Loader):
    def __init__(self, container: ContainerBuilder):
        self.__container = container

    def load(self, resource: str) -> None:
        try:
            resource_loaded: dict = self.__resource_loaded(resource) or {}
        except FileNotFoundError as e:
            raise exceptions.ResourceNotFound(resource) from e
        except yaml.YAMLError as e:
            raise exceptions.ParsingErrorOnResource(resource) from e

        for identifier, definition_content in resource_loaded.items():
            arguments = [
                Argument.no_kw_argument(arg)
                for arg in definition_content.get('args', [])
            ]

            arguments += [
                Argument(arg_name, arg_value)
                for arg_name, arg_value in definition_content.get('kwargs', {}).items()
            ]

            self.__container.set_definition(
                Definition(
                    identifier,
                    definition_content['fqn'],
                    arguments,
                )
            )

    def __resource_loaded(self, resource: str) -> dict:
        with open(resource, 'r') as stream:
            return yaml.safe_load(stream)

    def load_dir(self, directory: str) -> None:
        files = glob.glob(f'{directory}/**/[!_]*.yml', recursive=True)
        files.extend(glob.glob(f'{directory}/**/[!_]*.yaml', recursive=True))

        for file in files:
            self.load(file)
