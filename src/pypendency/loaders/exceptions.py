class ContainerLoaderError(Exception): pass


class ResourceNotFound(ContainerLoaderError):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(
            f"Resource {str(resource)} has not been found"
        )


class ParsingErrorOnResource(ContainerLoaderError):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(
            f"Resource {str(resource)} can't be parsed"
        )


class MissingLoaderMethod(ContainerLoaderError):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(
            f"Resource {str(resource)} requires loader method"
        )


class PathNotAbsolute(Exception):
    def __init__(self, path: str):
        self.path = path
        super().__init__(
            f"Path is not absolute: {path}"
        )
