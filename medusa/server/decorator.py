import functools
import json
from typing import Callable, List

from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from medusa.utils.json import process_request, serializer
from medusa.utils.merge import merge

from .logger import logger
from .server import url_map


def route(cls: type, rule: str, methods: List[str] = ["GET"], url_prefix: str = None) -> Callable:
    """A decorator for registering routes in the server.

    Args:
        - ``cls`` (type): The class associated with the route. Must always be ``cls``.
        - ``rule`` (str): The URL rule for the route.
        - ``methods`` (List[str], optional): The HTTP methods supported by the route. 
          Defaults to `['GET']`.
        - ``url_prefix`` (str): The URL prefix for the route. Defaults to `None`.

    Func Args:
        - ``args`` (dict): Source function positional arguments.
        - ``kwargs`` (dict): Source function key word arguments.

    Raises:
        - ``Exception``: If there is an issue while registering the route, an exception 
          is raised.

    Returns:
        ```Callable```: The decorator function.
    """

    if not url_prefix:
        rule = f"{cls.__url_prefix__()}{rule}"
    else:
        rule = f"{url_prefix}{rule}"
    if rule.startswith("//"):
        rule = rule[1:]
    try:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapped(request, *args, **kwargs):
                return build_response(cls, request, func, *args, **kwargs)
            register_route(cls, rule, wrapped, methods)
            return wrapped
        return decorator
    except Exception as e:
        logger.error(f"Failed to register {cls.__name__} route {rule}")
        pass


def build_response(cls, request, func, *args, **kwargs):
    request = process_request(request)
    result = func(cls, request, *args, **kwargs)
    if isinstance(result, Response):
        return result
    if isinstance(result, str) and result.strip().startswith("<"):
        return Response(
            result.strip(),
            content_type="text/html; charset=utf-8"
        )
    return Response(
        json.dumps(result, default=serializer),
        content_type="application/json; charset=utf-8"
    )


def register_route(cls, rule, wrapped, methods):
    if not any([rule == r.rule for r in url_map.iter_rules()]):
        url_map.add(Rule(rule, endpoint=wrapped, methods=methods))
        logger.debug(f"Registered {cls.__name__} route {rule}")


def merge_request(func):
    """A decorator that merges positional and keyword arguments.

    Args:
        ``func`` (function): The function to decorate.

    Returns:
        ``function``: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(cls, request, *args, **kwargs):
        args = request.get("args")
        form = request.get("form")
        json = request.get("json")
        request = merge(**args, **form, **json)
        return func(cls, request, *args, **kwargs)
    return wrapper
