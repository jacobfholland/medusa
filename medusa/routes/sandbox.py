from typing import Callable

from werkzeug.wrappers import Request, Response

from medusa.controllers.index import IndexController
from medusa.database.decorator import attribute
from medusa.server.decorator import route
from medusa.server.route import Route


class SandboxRoute(Route):
    """A route class representing the sandbox endpoint of the application.

    This class inherits from the ``Route`` base class and defines the sandbox endpoint.
    """

    @classmethod
    def routes(cls, __class__) -> Callable:
        @route(cls, "/sandbox", methods=["GET"])
        def sandbox(cls, request: Request) -> Response:
            """Handler function for the sandbox endpoint.

            Args:
                - ``request`` (Request): The HTTP request object.

            Returns:
                ``Response``: The HTTP response object.
            """

            return "Sandbox"

        super(cls, cls).routes(cls)
