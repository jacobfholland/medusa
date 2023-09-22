import functools
from typing import Any, Callable, Union

from .logger import logger
from .validation import evaluate, is_iterable, is_model

DEFAULT_KEY = "vals"
"""Default key to be used when no key exists

TODO:
    - Make this an environment variable    
"""


def merge(*args: Any, **kwargs: Any) -> dict:
    """Merges the input arguments into a single dictionary.

    Handles special cases for iterable and model objects. The function takes
    any number of arguments and keyword arguments and returns a dictionary that
    merges them all. If a key is found multiple times, it will join those values
    found into a list. If the value has no key, it will be bound to the `vals`
    attribute on the returned dictionary.

    Args:
        - ``*args`` (Any): Arbitrary positional arguments.
        - ``**kwargs`` (Any): Arbitrary keyword arguments.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens while 
          merging values.

    Returns:
        ``dict``: The new dictionary merging all inputs.
    """

    try:
        new_kwargs = {}
        for k, v in kwargs.items():
            evaluate_arg(new_kwargs, k, v)
        for v in args:
            evaluate_arg(new_kwargs, DEFAULT_KEY, v)
        return new_kwargs
    except Exception as e:
        logger.warning(f"Failed to merge *args and **kwargs: {e}")


def evaluate_arg(kwargs: dict, k: str, v: Any) -> None:
    """Evaluates and processes a single argument.

    The function takes a key-value pair and evaluates the value before adding it 
    to `kwargs`. Handles iterable and model object cases.

    Args:
        - ``kwargs`` (dict): Dictionary to which to append the value.
        - ``k`` (str): The key for the for the argument.
        - ``v`` (Any): The value to evaluate and add.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens 
          while evaluating the arg. 

    Returns:
        ``None``: Void.
    """

    try:
        v = evaluate(v)
        if is_iterable(v):
            handle_iterable(kwargs, k, v)
        elif is_model(v):
            handle_obj(v, kwargs)
        else:
            bind_value(kwargs, k, v)
    except Exception as e:
        logger.warning(f"Failed to evaluate arg: {e}")


def handle_iterable(kwargs: dict, k: str, arg: Union[list, tuple, set, dict]) -> None:
    """Handles iterable arguments for evalution.

    Args:
        - ``kwargs`` (dict): Dictionary to which to append the value.
        - ``k`` (str): The key in the kwargs dictionary.
        - ``arg`` (Union[list, tuple, set, dict]): The iterable argument.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens while 
          handling the iterable arg.


    Returns:
        ``None``: Void.
    """

    try:
        if isinstance(arg, (list, tuple, set)):
            for v in arg:
                evaluate_arg(kwargs, k, v)
        if isinstance(arg, dict):
            for k, v in arg.items():
                evaluate_arg(kwargs, k, v)
    except Exception as e:
        logger.warning(f"Failed to handle iterable: {e}")


def handle_obj(v: Any, kwargs: dict) -> None:
    """Handles object arguments.

    For each key-value pair in the object variables, it appends the value to 
    the `kwargs` dictionary if the key doesn't start with an underscore.

    Args:
        - ``v`` (Any): The object whose variables to handle.
        - ``kwargs`` (dict): Dictionary to which to append the values.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens while 
          handling the object arg.

    Returns:
        ``None``: Void.
    """

    try:
        for k, v in vars(v).items():
            if is_iterable(v):
                handle_iterable(k, v, kwargs)
            else:
                bind_value(kwargs, k, v)
    except Exception as e:
        logger.warning(f"Failed to handle object: {v}")


def bind_value(kwargs: dict, k: str, v: Any) -> None:
    """Binds a value to a key in the `kwargs` dictionary.

    Args:
        - ``kwargs`` (dict): Dictionary to which to append the values.
        - ``k`` (str): The key for appending to the `kwargs` dictionary.
        - ``v`` (Any): The value to be bound.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens while 
          handling the iterable arg.

    Returns:
        ``None``: Void.
    """

    try:
        if kwargs.get(k):
            if isinstance(kwargs[k], list):
                kwargs[k].append(v)
            else:
                if not k:
                    bind_value(kwargs, DEFAULT_KEY, v)
                else:
                    kwargs[k] = [kwargs[k], v]
        else:
            kwargs[k] = v
    except Exception as e:
        logger.warning(f"Failed to bind arg to values: {e}")


def merge_values(func: Callable):
    """Decorator that auto merges arguments. Merges the input arguments into a single 
    dictionary. Uses the `merge()` functionality.

    Handles special cases for iterable and model objects. The function takes
    any number of arguments and keyword arguments and returns a dictionary that
    merges them all. If a key is found multiple times, it will join those values
    found into a list. If the value has no key, it will be bound to the `vals`
    attribute on the returned dictionary.

    Args:
        - ``func`` (``Callable``): The function being decorated

    Func Args:
        - ``*args`` (Any): Arbitrary positional arguments.
        - ``**kwargs`` (Any): Arbitrary keyword arguments.

    Raises:
        - ``Exception``: Catch-all exception if anything unexpect happens while 
          merging values.

    Returns:
        ``None``: Void.
    """

    try:
        @functools.wraps(func)
        def wrapper(cls, *args, **kwargs):
            kwargs = merge(*args, **kwargs)
            return func(cls, *args, **kwargs)
        return wrapper
    except Exception as e:
        logger.warning(f"Failed to merge values in decorator: {e}")


def merge_request(request, *args, **kwargs):
    """Merges a request into a more managable data format.

    Args:
        ``func`` (function): The function to decorate.

    Returns:
        ``function``: The decorated function.
    """

    args = request.get("args")
    form = request.get("form")
    json = request.get("json")
    request = merge(**args, **form, **json)
    return request

# def merge_filter(func):
#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
#         request_args, request_kwargs = merge_request_args_kwargs(request)
#         request_args = [merge(request_args)]
#         request_kwargs = merge(request_kwargs)
#         return func(*request_args, **request_kwargs)
#     return wrapper
