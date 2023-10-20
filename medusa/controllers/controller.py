

import functools
from typing import Callable
from medusa.utils.merge import merge, merge_values


class Controller:
    """Base controller class to either be inherited by `Model` or used on it's own."""

    @classmethod
    @merge_values
    def create(cls, *args, **kwargs):
        _import_class = kwargs.get("_import_class")
        return _import_class.create(**kwargs)

    @classmethod
    @merge_values
    def get(cls, *args, **kwargs):
        _import_class = kwargs.get("_import_class")
        return _import_class.get(**kwargs)

    @classmethod
    @merge_values
    def update(cls, *args, **kwargs):
        _import_class = kwargs.get("_import_class")
        return _import_class.update(**kwargs)

    @classmethod
    @merge_values
    def delete(cls, *args, **kwargs):
        _import_class = kwargs.get("_import_class")
        return _import_class.delete(**kwargs)
