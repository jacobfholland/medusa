from app.utils.format import snake_case


class Route:
    @classmethod
    def __url_prefix__(cls) -> str:
        """Generate the URL prefix for the route based on the class name. Defaults to 
        `/<class_name>` but is meant to be overridden in subclasses to define a specific
        URL prefix

        Returns:
            str: The generated URL prefix for the route.
        """

        return f"/{snake_case(cls.__name__)}"

    @classmethod
    def routes(cls) -> None:
        """Define routes for the `Route``.

        Args:
            cls (type): The class associated with the routes. Must always be `cls`.

        Returns:
            bool: True if routes are successfully defined.
        """

        pass
