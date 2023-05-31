from typing import Union

from pypendency.definition import Definition
from pypendency.tag import Tag


class ContainerAlreadyResolved(Exception):
    def __init__(self):
        super().__init__("Container already resolved can't be resolved again")


class ForbiddenChangeOnResolvedContainer(Exception):
    def __init__(self):
        super().__init__("Container can't be modified once resolved")


class ServiceAlreadyDefined(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(
            f"The service identified by {identifier} has already been defined in container"
        )


class ServiceNotFoundInContainer(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(
            f"The service identified by {identifier} has not been defined in container"
        )


class ServiceNotFoundFromFullyQualifiedName(Exception):
    def __init__(self, fully_qualified_name: str):
        self.fully_qualified_name = fully_qualified_name
        super().__init__(
            f"Container can't locate any class in {fully_qualified_name}"
        )


class ServiceInstantiationFailed(Exception):
    def __init__(self, service_fqn: str) -> None:
        self.service_fqn = service_fqn
        super().__init__(f"Type {service_fqn} cannot be instantiated by the container")


class TagNotFoundInContainer(Exception):
    def __init__(self, tag_identifier: str) -> None:
        self.tag_identifier = tag_identifier
        super().__init__(f"The tag '{tag_identifier}' does not exist in the container")


class PypendencyCallbackException(Exception):
    def __init__(self) -> None:
        super().__init__(f"Exception on_resolved_callback")
