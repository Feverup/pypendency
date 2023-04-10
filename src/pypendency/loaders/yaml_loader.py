import glob
import yaml

from pypendency.argument import Argument
from pypendency.builder import ContainerBuilder
from pypendency.definition import Definition
from pypendency.loaders import exceptions
from pypendency.loaders.loader import Loader
from pypendency.tag import Tag


class YamlLoader(Loader):
    def __init__(self, container: ContainerBuilder):
        self.__container = container

    def load(self, resource: str) -> None:
        self._guard_path_is_absolute(resource)
        self.__load_by_absolute_path(resource)

    def __load_by_absolute_path(self, resource: str) -> None:
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

            tags = {
                Tag(identifier=identifier, value=value)
                for identifier, value in definition_content.get('tags', {}).items()
            }

            self.__container.set_definition(
                Definition(
                    identifier,
                    definition_content['fqn'],
                    arguments,
                    tags,
                )
            )

    def __resource_loaded(self, resource: str) -> dict:
        with open(resource, 'r') as stream:
            return yaml.safe_load(stream)

    def load_dir(self, directory: str) -> None:
        self._guard_path_is_absolute(directory)
        files = glob.glob(f'{directory}/**/[!_]*.yml', recursive=True)
        files.extend(glob.glob(f'{directory}/**/[!_]*.yaml', recursive=True))

        for file in files:
            self.__load_by_absolute_path(file)
