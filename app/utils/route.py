import functools
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
import json
from app.utils.json import serializer


def route(obj, rule, methods=['GET'], *args, **kwargs):
    prefix = kwargs.get("url_prefix")
    if not prefix:
        prefix = obj.__url_prefix__
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
    return decorator
