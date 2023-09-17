from app.server.decorators import route
from app.server.route import Route
from utils.format import snake_case


class Home(Route):
    def __init__(self):
        super().__init__()

    @classmethod
    def __url_prefix__(cls):
        return f"/poop"

    @classmethod
    def routes(cls):
        @route(cls, "/hello", methods=["GET"])
        def hello(request):
            return "<html>OK<html>"
