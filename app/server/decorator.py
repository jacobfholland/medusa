import functools
import json
from typing import Callable, List

from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from app.utils.json import serializer

from .logger import logger
from .server import url_map


def route(cls: type, rule: str, methods: List[str] = ["GET"], *args, **kwargs) -> Callable:
    """
    A decorator for registering routes in the server.

    Args:
        cls (type): The class associated with the route.
        rule (str): The URL rule for the route.
        methods (List[str], optional): The HTTP methods supported by the route (default is ['GET']).
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments, including 'url_prefix' to specify a custom URL prefix.

    Returns:
        Callable: The decorator function.

    Raises:
        Exception: If there is an issue while registering the route, an exception is raised.
    """

    try:
        prefix = kwargs.get("url_prefix")
        if not prefix:
            prefix = cls.__url_prefix__()
        rule = f"{prefix}{rule}"

        def decorator(f: Callable) -> Callable:
            """
            Decorator function for registering a route.

            Args:
                f (Callable): The function handling the route.

            Returns:
                Callable: The wrapped function for handling the route.
            """
            @functools.wraps(f)
            def wrapped(request, *args, **kwargs):
                result = f(request, *args, **kwargs)
                if isinstance(result, Response):
                    return result
                if isinstance(result, str) and result.strip().startswith("<"):
                    return Response(result, content_type="text/html; charset=utf-8")
                return Response(json.dumps(result, default=serializer), content_type="application/json; charset=utf-8")

            if not any([rule == r.rule for r in url_map.iter_rules()]):
                url_map.add(Rule(rule, endpoint=wrapped, methods=methods))
            logger.debug(f"Registered {cls.__name__} route {rule}")
            return wrapped

        return decorator
    except Exception as e:
        logger.error(
            f"Failed to register {cls.__name__} route {rule}")
        pass
