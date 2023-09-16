from app.server.decorators import route
from app.server.route import Route


class TestRoute(Route):
    __url_prefix__ = ""

    def __init__(self):
        super().__init__()

    def routes(self):
        @route(self, "/hello", methods=["GET"])
        def hello(request):
            return "<html>Hello<html>"
