from app.route.decorators import route
from app.route.route import Route


class TestRoute(Route):
    __url_prefix__ = "/hello"

    def routes(self):
        @route(self, "/get", methods=["GET"])
        def hello(request):
            return "<html>Hello<html>"
