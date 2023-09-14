import functools
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
import json


def route(rule, methods=['GET']):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)

            # If it's already a Response object, return it as-is
            if isinstance(result, Response):
                return result

            # Check if result looks like HTML (rudimentary check)
            if isinstance(result, str) and result.strip().startswith("<"):
                return Response(result, content_type='text/html; charset=utf-8')

            # Default to JSON for other Python data types (dicts, lists, etc.)
            return Response(json.dumps(result), content_type='application/json; charset=utf-8')

        if not any([rule == r.rule for r in url_map.iter_rules()]):
            url_map.add(Rule(rule, endpoint=wrapped, methods=methods))

        return wrapped

    return decorator
