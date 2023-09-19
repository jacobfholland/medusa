from typing import Callable

from werkzeug.wrappers import Request, Response

from medusa.controllers.index import IndexController
from medusa.server.decorator import route
from medusa.server.route import Route


class IndexRoute(Route):
    """A route class representing the index endpoint of the application.

    This class inherits from the `Route` base class and defines the index endpoint ("/").
    """

    def __init__(self) -> None:
        """Initialize a new IndexRoute instance.

        Returns:
            `None`
        """

        super().__init__()

    @classmethod
    def __url_prefix__(cls) -> str:
        """Define the URL prefix for the index route.

        Returns:
            `str`: The URL prefix for the index route (empty string).
        """

        return ""

    @classmethod
    def routes(cls) -> Callable:
        """Define routes for handling HTTP requests at the index endpoint.

        Args:
            - `cls` (type): The class associated with the routes. Must always be `cls`.

        Returns:
            `super()`: Parent `routes()` method
        """

        @route(cls, "/", methods=["GET"])
        def index(request: Request) -> Response:
            """Handler function for the index endpoint.

            Args:
                - `request` (Request): The HTTP request object.

            Returns:
                `Response`: The HTTP response object.
            """

            return IndexController.index(request)
        return super().routes()
