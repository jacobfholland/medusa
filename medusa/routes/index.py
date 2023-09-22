from typing import Callable

from werkzeug.wrappers import Request, Response

from medusa.controllers.index import IndexController
from medusa.database.decorator import attribute
from medusa.server.decorator import route
from medusa.server.route import Route


class IndexRoute(Route):
    """A route class representing the index endpoint of the application.

    This class inherits from the ``Route`` base class and defines the index endpoint.
    """

    @classmethod
    def routes(cls, __class__) -> Callable:

        @route(cls, "/index", methods=["GET"])
        def index(cls, request: Request) -> Response:
            """Handler function for the index endpoint.

            Args:
                - ``request`` (Request): The HTTP request object.

            Returns:
                ``Response``: The HTTP response object.
            """

            return IndexController.index(request)

        super(cls, cls).routes(cls)
