from app.server.decorator import route
from app.server.route import Route
from app.utils.format import snake_case


class Root(Route):
    def __init__(self):
        super().__init__()

    @classmethod
    def __url_prefix__(cls):
        return f""

    @classmethod
    def routes(cls):
        @route(cls, "/", methods=["GET"])
        def root(request):
            return "<html>HOME<html>"
