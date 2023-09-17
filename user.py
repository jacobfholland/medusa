from app.database.model import Model
from app.server.decorator import route


class User(Model):
    def __init__(self):
        super().__init__()

    @classmethod
    def routes(cls):
        """Defines custom User routes

        Args:
            cls (type): The class associated with the routes. Must always be `cls`.

        Returns:
            super(): Parent `routes()` method
        """

        @route(cls, "/login", methods=["GET"])
        def login(request):
            return "<html>LOGIN<html>"

        @route(cls, "/logout", methods=["POST"])
        def logout(request):
            return "<html>LOGOUT<html>"
        return super().routes()
