from app.route.decorators import route
from app.route.route import Route


class TestRoute(Route):
    __url_prefix__ = ""

    def routes(self):
        @route(self, "/hello", methods=["GET"])
        def hello(request):
            return "<html>Hello<html>"
