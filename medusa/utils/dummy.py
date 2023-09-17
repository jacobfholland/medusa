class DummyRoute:
    """A dummy class to be imported when the Server package is otherwise not installed."""

    @classmethod
    def routes(cls):
        """Placeholder method for registering routes.

        Subclasses should override this method to register their specific routes with the server.
        """
        pass
