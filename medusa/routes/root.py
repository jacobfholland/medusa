from typing import Callable

from werkzeug.wrappers import Request, Response

from medusa.server.decorator import route
from medusa.server.route import Route


class Root(Route):
    """A route class representing the root endpoint of the application.

    This class inherits from the `Route` base class and defines the root endpoint ("/").
    """

    def __init__(self) -> None:
        """Initialize a new Root instance.

        Returns:
            None
        """
        super().__init__()

    @classmethod
    def __url_prefix__(cls) -> str:
        """Define the URL prefix for the root route.

        Returns:
            str: The URL prefix for the root route (empty string).
        """
        return ""

    @classmethod
    def routes(cls) -> Callable:
        """Define routes for handling HTTP requests at the root endpoint.

        Args:
            cls (type): The class associated with the routes. Must always be `cls`.

        Returns:
            super(): Parent `routes()` method
        """
        @route(cls, "/", methods=["GET"])
        def root(request: Request) -> Response:
            """Handler function for the root endpoint.

            Args:
                request (Request): The HTTP request object.

            Returns:
                Response: The HTTP response object.
            """

            return "<html>HOME<html>"
        return super().routes()
