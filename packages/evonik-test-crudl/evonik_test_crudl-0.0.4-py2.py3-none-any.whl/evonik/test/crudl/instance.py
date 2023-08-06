import pytest


class Instance:
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """
    def __init__(self, component, **values):
        self.component = component
        self.values = values if values else {}

    def __enter__(self):
        self.spec = self.component.endpoints.create.dummy.valids()[0]
        for k, v in self.values.items():
            self.spec[k] = v

        self._referenced_instances = {}
        for k, reference in self.component.references.items():
            if k not in self.spec:
                instance = Instance(reference)
                self._referenced_instances[k] = instance
                instance.__enter__()
                self.spec[k] = instance.data["id"]

        self.data = self.component.endpoints.create.call(self.spec)
        return self

    def __exit__(self, type, value, traceback):
        for referenced_instance in self._referenced_instances.values():
            referenced_instance.__exit__(None, None, None)
        self.component.endpoints.delete.call(self.data)

    def get_references(self):
        return {**self.references, **self._references}
