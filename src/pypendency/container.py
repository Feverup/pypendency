from abc import ABC, abstractmethod
from pydoc import locate
from typing import Any, Dict, List, Optional, Union, Set, Tuple

from pypendency import exceptions
from pypendency.argument import Argument
from pypendency.definition import Definition
from pypendency.tag import Tag


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
        self._tags_mapping: Dict[Tag, List[str]] = {}

    def resolve(self) -> None:
        if self.is_resolved():
            raise exceptions.ContainerAlreadyResolved()

        self.__populate_tags_map()
        self._resolved = True

    def is_resolved(self) -> bool:
        return self._resolved

    def __populate_tags_map(self) -> None:
        for service in self._service_mapping.values():
            if not isinstance(service, Definition):
                continue
            for tag in service.tags:
                self.__add_service_to_tag_group(tag, service.identifier)

    def __add_service_to_tag_group(self, tag: Tag, service_identifier: str) -> None:
        self._tags_mapping.setdefault(tag, set()).add(service_identifier)

    def set(self, identifier: str, service: object, tags: Optional[Set[Tag]] = None) -> None:
        if self.is_resolved():
            raise exceptions.ForbiddenChangeOnResolvedContainer()

        if self.has(identifier):
            raise exceptions.ServiceAlreadyDefined(identifier)

        self._service_mapping.update({identifier: service})
        if tags is not None:
            for tag in tags:
                self.__add_service_to_tag_group(tag, identifier)

    def get(self, identifier: str) -> Optional[object]:
        if self.is_resolved() is False:
            self.resolve()

        return self._do_get(identifier)

    def get_by_tag(self, tag: Tag) -> Set[object]:
        if self.is_resolved() is False:
            self.resolve()

        if tag not in self._tags_mapping:
            raise exceptions.TagNotFoundInContainer(tag.identifier)

        return set([self._do_get(service) for service in self._tags_mapping[tag]])

    def get_by_tag_name(self, tag_identifier: str, tag_value: Optional[object] = Tag.UNSET_VALUE) -> Set[object]:
        if self.is_resolved() is False:
            self.resolve()

        services = set()
        for tag, tagged_services in self._tags_mapping.items():
            if tag.identifier == tag_identifier and (tag_value == Tag.UNSET_VALUE or tag.value == tag_value):
                for tagged_service in tagged_services:
                    services.add(self._do_get(tagged_service))

        return services

    def get_service_tags(self, service_identifier: str) -> Set[Tag]:
        if self.is_resolved() is False:
            self.resolve()

        return {tag for tag, services in self._tags_mapping.items() if service_identifier in services}

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

        try:
            return klass(*args, **kwargs)
        except TypeError as e:
            raise exceptions.ServiceInstantiationFailed(fully_qualified_name) from e

    def has(self, identifier: str) -> bool:
        return identifier in self._service_mapping
