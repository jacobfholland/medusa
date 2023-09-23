from typing import Callable

from werkzeug.wrappers import Request, Response

from medusa.server.decorator import route
from medusa.server.route import Route


class UserRoute(Route):
    """A route class representing the index endpoint of the application.

    This class inherits from the ``Route`` base class and defines the index endpoint.
    """

    url_prefix = "/user"

    @classmethod
    def routes(cls, _class) -> Callable:
        @route(cls, "/get", methods=["GET"])
        def get(cls, request: Request) -> Response:
            """Handler function for the test endpoint.

            Args:
                - ``request`` (Request): The HTTP request object.

            Returns:
                ``Response``: The HTTP response object.
            """

            return "TEST"

        super(cls, cls).routes(_class)
