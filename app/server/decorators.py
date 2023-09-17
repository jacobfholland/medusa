import functools
import json

from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from utils.json import serializer

from app.server.logger import logger
from app.server.server import url_map


def route(cls, rule, methods=['GET'], *args, **kwargs):
    try:
        prefix = kwargs.get("url_prefix")
        if not prefix:
            prefix = cls.__url_prefix__()
        rule = f"{prefix}{rule}"

        def decorator(f):
            @functools.wraps(f)
            def wrapped(request, *args, **kwargs):
                result = f(request, *args, **kwargs)
                if isinstance(result, Response):
                    return result
                if isinstance(result, str) and result.strip().startswith("<"):
                    return Response(result, content_type='text/html; charset=utf-8')
                return Response(json.dumps(result, default=serializer), content_type='application/json; charset=utf-8')
            if not any([rule == r.rule for r in url_map.iter_rules()]):
                url_map.add(Rule(rule, endpoint=wrapped, methods=methods))
            return wrapped
        logger.debug(f"Registered route {cls.__name__} route {rule}")
        return decorator
    except Exception as e:
        logger.error(
            f"Failed to register {cls.__name__} route {rule}")
        pass
