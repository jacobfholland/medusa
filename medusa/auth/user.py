from typing import Callable
from medusa.database.model import Model
from medusa.server.decorator import route
from medusa.server.route import Route
from medusa.utils.format import snake_case


class User(Model):
    """User model in the application.

    This class inherits from the `Model` base class, which provides common fields 
    and functionality for database models. It is used to define and interact with 
    user data in the database.

    Methods:
        - ``routes``: Define custom User routes.
    """

    url_prefix = "/user"

    def __init__(self) -> None:
        """Initialize a new `User` instance.

        Returns:
            ``None``: Void.
        """

        super().__init__()

    @classmethod
    def routes(cls, __class__) -> Callable:
        @route(__class__, "/login", methods=["GET"])
        def login(__class__, request):
            """Handler function for the get endpoint.

            Args:
                - ``request`` (Request): The HTTP request object.

            Returns:
                ``Response``: The HTTP response object.
            """
            return "login"
        super(cls, __class__).routes()
