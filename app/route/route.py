from app.server.werzeug import url_map
from .logger import logger
from app.utils.format import snake_case
import functools
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
import json
from app.utils.json import serializer


def route(obj, rule, methods=['GET'], *args, **kwargs):
    try:
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
        logger.debug(f"Registered class {obj.__class__.__name__} route {rule}")
        return decorator
    except Exception as e:
        logger.error(
            f"Failed to register {obj.__class__.__name__} route {rule}")


class Route:
    def __init__(self):
        self.url_map = url_map
        try:
            self.register_crud()
            self.routes()
        except Exception as e:
            logger.error(
                f"Failed to register CRUD routes for {self.__class__.__name__}: {e}")

    @property
    def __url_prefix__(self):
        return f"/{snake_case(self.__class__.__name__)}"

    def register_crud(self):
        @route(self, "/create", methods=["POST"])
        def create(request):
            return "<html>OK<html>"

        @route(self, "/get", methods=["GET"])
        def get(request):
            return "<html>OK<html>"

        @route(self, "/update", methods=["PUT", "PATCH"])
        def update(request):
            return "<html>OK<html>"

        @route(self, "/delete", methods=["DELETE"])
        def delete(request):
            return "<html>OK<html>"

    def routes(self):
        pass
