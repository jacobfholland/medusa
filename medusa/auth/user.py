from medusa.database.model import Model
from medusa.server.decorator import route


class User(Model):
    """User model in the application.

    This class inherits from the `Model` base class, which provides common fields 
    and functionality for database models. It is used to define and interact with 
    user data in the database.

    Methods:
        - ``routes``: Define custom User routes.
    """

    def __init__(self) -> None:
        """Initialize a new `User` instance.

        Returns:
            ``None``: Void.
        """
        super().__init__()

    @classmethod
    def routes(cls):
        """Defines custom `User` routes.

        Args:
            - ``cls``: (type): The class associated with the routes. Must always be 
              ``cls``.

        Returns:
            ``super``: Parent `routes()` method.
        """

        @route(cls, "/login", methods=["GET"], url_prefix="/")
        def login(request):
            return "<html>LOGIN<html>"

        @route(cls, "/logout", methods=["POST"], url_prefix="/")
        def logout(request):
            return "<html>LOGOUT<html>"
        return super().routes()
