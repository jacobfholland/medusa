from medusa.controllers.controller import Controller
from medusa.database.decorator import attribute
from medusa.utils.format import snake_case
from medusa.utils.merge import merge_request
from medusa.utils.printable import Printable
from medusa.server.config import Config
from medusa.server.decorator import route


class Route(Printable):
    """A base class for defining routes in the application.

    This class provides a foundation for defining URL prefixes and routes for 
    specific endpoints.

    Methods:
        - ``__url_prefix__``: Generate the URL prefix for the route based on the 
          class name.
        - ``routes``: Define routes for the `Route` subclass.

    Notes:
        - Subclasses of `Route` should override the `__url_prefix__()` method to 
          define specific
        - URL prefixes for their routes.
        - Subclasses of `Route` should override the `routes()` method to define 
          specific routes.
    """

    url_prefix = "/"
    __abstract__ = True

    @attribute
    def controller(cls):
        return Controller

    @classmethod
    def routes(cls, __class__):

        if "Model" in [name.__name__ for name in __class__.mro()]:

            @route(__class__, "/", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
            def index(__class__, request):
                """Handler function for the index endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                # TODO Handle all request types in the index
                request = merge_request(request)
                return __class__.controller.index(request)

            @route(__class__, "/create", methods=["POST"])
            def create(__class__, request):
                """Handler function for the create endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return __class__.controller.create(request)

            @route(__class__, "/get", methods=["GET"])
            def get(__class__, request):
                """Handler function for the get endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return __class__.controller.get(request)

            @route(__class__, "/update", methods=["PATCH", "PUT"])
            def update(__class__, request):
                """Handler function for the update endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return __class__.controller.update(request)

            @route(__class__, "/delete", methods=["GET"])
            def delete(__class__, request):
                """Handler function for the get endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return __class__.controller.delete(request)
