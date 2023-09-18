from medusa.utils.format import snake_case


class Route:
    """A base class for defining routes in the application.

    This class provides a foundation for defining URL prefixes and routes for specific endpoints.

    Methods:
        - `__url_prefix__()`: Generate the URL prefix for the route based on the class name.
        - `routes()`: Define routes for the `Route` subclass.

    Notes:
        - Subclasses of `Route` should override the `__url_prefix__()` method to define specific
        - URL prefixes for their routes.
        - Subclasses of `Route` should override the `routes()` method to define specific routes.
    """

    @classmethod
    def __url_prefix__(cls) -> str:
        """Generate the URL prefix for the route based on the class name. Defaults to 
        `/<class_name>` but is meant to be overridden in subclasses to define a specific
        URL prefix

        Returns:
            `str`: The generated URL prefix for the route.
        """

        return f"/{snake_case(cls.__name__)}"

    @classmethod
    def routes(cls) -> None:
        """Define routes for the `Route``.

        Args:
            - `cls` (type): The class associated with the routes. Must always be `cls`.

        Returns:
            `None`
        """

        pass
