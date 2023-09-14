from app.server.werzeug import url_map
from app.utils.route import route
from app.server.logger import logger
from app.utils.format import snake_case


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
