import inspect
from typing import Any


def is_iterable(arg: Any) -> bool:
    """Checks if the given argument is iterable, or if it has 'is_model' key.

    Args:
        - `arg` (Any): Argument to check.

    Returns:
        `bool`: True if the argument is iterable or has 'is_model' key, False otherwise.
    """

    if isinstance(arg, (list, set, tuple, dict)):
        return True
    return False


def is_model(obj: Any) -> bool:
    """Checks if the given object is an instance of 'Model' class.

    Args:
        - `obj` (Any): Object to check.

    Returns:
        `bool`: True if the object is an instance of 'Model', False otherwise.
    """

    for cls in inspect.getmro(obj.__class__):
        if cls.__name__ == 'Model':
            return True
    return False
