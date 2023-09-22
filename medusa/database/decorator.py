import functools


def attribute(func):
    """A decorator that applies both @classmethod and @property decorators to a 
    method.
    """

    @classmethod
    @property
    @functools.wraps(func)
    def wrapper(cls):
        return func(cls)
    return wrapper
