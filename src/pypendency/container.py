from abc import ABC, abstractmethod
from pydoc import locate
from typing import Any, Dict, List, Optional, Union

from pypendency import exceptions
from pypendency.argument import Argument
from pypendency.definition import Definition


class AbstractContainer(ABC):
    @abstractmethod
    def set(self, identifier: str, service: object) -> None: pass

    @abstractmethod
    def get(self, identifier: str) -> Optional[object]: pass

    @abstractmethod
    def has(self, identifier: str) -> bool: pass


class Container(AbstractContainer):
    def __init__(self, definitions: List[Definition]):
        self._resolved = False
        self._service_mapping: Dict[str, Union[None, object, Definition]] = {
            definition.identifier: definition
            for definition in definitions
        }

    def resolve(self) -> None:
        if self.is_resolved():
            raise exceptions.ContainerAlreadyResolved()

        self._resolved = True

    def is_resolved(self) -> bool:
        return self._resolved

    def set(self, identifier: str, service: object) -> None:
        if self.is_resolved():
            raise exceptions.ForbiddenChangeOnResolvedContainer()

        if self.has(identifier):
            raise exceptions.ServiceAlreadyDefined(identifier)

        self._service_mapping.update({identifier: service})

    def get(self, identifier: str) -> Optional[object]:
        if self.is_resolved() is False:
            self.resolve()

        return self._do_get(identifier)

    def _do_get(self, identifier: str) -> Optional[object]:
        empty = object()

        service = self._service_mapping.get(identifier, empty)

        if service is empty:
            raise exceptions.ServiceNotFoundInContainer(identifier)

        if not isinstance(service, Definition):
            return service

        definition = service
        args, kwargs = [], {}
        for argument in definition.arguments:
            argument: Argument = argument
            value = self.__get_argument_value(argument)
            if argument.key is None:
                args.append(value)
                continue

            kwargs.update({argument.key: value})

        instance = self.__instance_from_fqn(definition.fully_qualified_name, args, kwargs)
        self._service_mapping.update({identifier: instance})

        return instance

    def __get_argument_value(self, argument: Argument) -> Any:
        if isinstance(argument.value, str) and argument.value.startswith("@"):
            return self.get(argument.value[1:])

        return argument.value

    def __instance_from_fqn(self, fully_qualified_name: str, args: list, kwargs: dict) -> Any:
        klass = locate(fully_qualified_name)

        if klass is None:
            raise exceptions.ServiceNotFoundFromFullyQualifiedName(fully_qualified_name)

        return klass(*args, **kwargs)

    def has(self, identifier: str) -> bool:
        return identifier in self._service_mapping
