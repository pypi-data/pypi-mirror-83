import pytest


class Endpoint:
    """Specification of endpoints of an API.

    The following endpoints with specific meaning can be specified:

    1. create, signature: create(spec)
    2. read, signature:      get(data)
    2. update, signature: update(data, spec)
    3. delete, signature: delete(data)
    5. list, signature:     list(spec)
    """

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

    def __init__(self, endpoint,
                 dummy=None,
                 dependencies=None):
        self.endpoint = endpoint
        self.dummy = dummy
        self.dependencies = dependencies if dependencies else []

    def call(self, *args, **kwargs):
        return self.endpoint(*args, **kwargs)


class Endpoints:
    """Short Description.

    Detailed description.

    Parameters
    ----------
    x: type, default value
        Description what the function does
    
    Examples
    --------
    how_to_call(...)
    """
    def __init__(self, **endpoints):
        for k, v in endpoints.items():
            setattr(self, k, v)
