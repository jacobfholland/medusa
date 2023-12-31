from medusa.controllers.controller import Controller
from medusa.database.decorator import attribute
from medusa.server.decorator import route
from medusa.utils.format import snake_case
from medusa.utils.merge import merge_request
from medusa.utils.printable import Printable


class Route(Printable):
    """A base class for defining routes in the application.

    This class provides a foundation for defining URL prefixes and routes for 
    specific endpoints.

    Methods:
        - ``url_prefix``: Generate the URL prefix for the route based on the 
          class name.
        - ``routes``: Define routes for the `Route` subclass.

    Notes:
        - Subclasses of `Route` should override the `url_prefix` method to 
          define specific
        - URL prefixes for their routes.
        - Subclasses of `Route` should override the `routes()` method to define 
          specific routes.
    """

    __abstract__ = True
    url_prefix = "/"

    @attribute
    def controller(cls):
        return Controller

    @classmethod
    def routes(cls, import_class):
        if "Model" in [name.__name__ for name in import_class.mro()]:
            @route(import_class, "/", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
            def index(import_class, request):
                """Handler function for the index endpoint.

                Args:
                    - ``import_class``: Class that contains the controller for handling HTTP methods.
                    - ``request`` (Request): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                data = merge_request(request)
                data["_import_class"] = import_class
                methods = {
                    "POST": import_class._controller.create,
                    "GET": import_class._controller.get,
                    "PUT": import_class._controller.update,
                    "PATCH": import_class._controller.update,
                    "DELETE": import_class._controller.delete
                }
                controller_method = methods.get(
                    request.get("method")
                )
                return controller_method(data)

            @route(import_class, "/create", methods=["POST"])
            def create(import_class, request):
                """Handler function for the create endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)

                return import_class._controller.create(request)

            @route(import_class, "/get", methods=["GET"])
            def get(import_class, request):
                """Handler function for the get endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return import_class._controller.get(request)

            @route(import_class, "/update", methods=["PATCH", "PUT"])
            def update(import_class, request):
                """Handler function for the update endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return import_class._controller.update(request)

            @route(import_class, "/delete", methods=["DELETE"])
            def delete(import_class, request):
                """Handler function for the get endpoint.

                Args:
                    - ``request`` (``Request``): The HTTP request object.

                Returns:
                    ``Response``: The HTTP response object.
                """

                request = merge_request(request)
                return import_class._controller.delete(request)
