import ast
import functools

from .logger import logger
from .validation import eval, is_iterable, is_model


def merge(*args: any, **kwargs: any) -> dict:
    """
    Merges the input arguments into a single dictionary, handling special 
    cases for iterable and model objects.

    Args:
        *args (any): Variable length argument list.
        **kwargs (any): Arbitrary keyword arguments.

    Returns:
        dict: The new dictionary merging all inputs.
    """

    new_kwargs = {}
    for k, v in kwargs.items():
        if is_iterable(v):
            handle_iterable(k, v, new_kwargs)
        elif is_model(v):
            handle_obj(v, new_kwargs)
        else:
            append_value_to_list(new_kwargs, k, v)
    for v in args:
        # TODO: Is model?
        if is_iterable(v):
            handle_iterable("vals", v, new_kwargs)
        else:
            append_value_to_list(new_kwargs, "vals", v)
    return new_kwargs


def append_value_to_list(new_kwargs: dict, k: str, v: any) -> None:
    """
    Appends a value to a list in new_kwargs. If the key is not present, it 
    adds the key with the value. If the key is present and its value is not 
    a list, it converts the value to a list and appends the new value.

    Args:
        new_kwargs (dict): Dictionary to which to append the value.
        k (str): The key in the dictionary.
        v (any): The value to append.

    Returns:
        None
    """

    if new_kwargs.get(k):
        if isinstance(new_kwargs[k], list):
            new_kwargs[k].append(v)
        else:
            if not k:
                append_value_to_list(new_kwargs, "vals", v)
            else:
                new_kwargs[k] = [new_kwargs[k], v]
    else:
        v = eval(v)
        new_kwargs[k] = v


def handle_iterable(k: str, arg: list | tuple | set | dict, new_kwargs: dict) -> None:
    """
    Handles iterable arguments. For dictionaries, it also appends the items 
    to the new_kwargs dictionary.

    Args:
        k (str): The key in the new_kwargs dictionary.
        arg (list | tuple | set | dict): The iterable argument.
        new_kwargs (dict): Dictionary to which to append the value.

    Returns:
        None
    """

    if isinstance(arg, (list, tuple, set)):
        if isinstance(arg, tuple):
            for v in arg:
                if is_iterable(v):
                    handle_iterable(k, v, new_kwargs)
            handle_iterable("new_args", v, new_kwargs)
        for v in arg:
            if is_iterable(v):
                handle_iterable(k, v, new_kwargs)
            else:
                append_value_to_list(new_kwargs, k, v)
    elif isinstance(arg, dict):
        for k, v in arg.items():
            if is_iterable(v):
                handle_iterable(k, v, new_kwargs)
            else:
                append_value_to_list(new_kwargs, k, v)


def handle_obj(v: any, new_kwargs: dict) -> None:
    """
    Handles object arguments. For each key-value pair in the object 
    variables, it appends the value to the new_kwargs dictionary if the key 
    doesn't start with an underscore.

    Args:
        v (any): The object whose variables to handle.
        new_kwargs (dict): Dictionary to which to append the values.

    Returns:
        None
    """

    for key, value in vars(v).items():
        if is_iterable(value):
            handle_iterable(key, value, new_kwargs)
        else:
            if not key.startswith("_"):
                append_value_to_list(new_kwargs, key, value)


# def merge_filter(func):
#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
#         request_args, request_kwargs = merge_request_args_kwargs(request)
#         request_args = [merge(request_args)]
#         request_kwargs = merge(request_kwargs)
#         return func(*request_args, **request_kwargs)
#     return wrapper


def merge_values(func):
    """
    A decorator that merges positional and keyword arguments.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = merge(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper
