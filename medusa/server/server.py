import sys
from typing import Callable

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

from medusa.server.logger import logger

url_map = Map()  # Application URL Map (registered endpointds)


class Server:
    """
    A class representing the WSGI server for the application.

    This class is responsible for handling HTTP requests and starting the server.

    Methods:
        - `application(environ, start_response)`: Main application method for handling HTTP requests.
        - `run()`: Start the server and listen for incoming requests.
    """

    def application(self, environ: dict, start_response: Callable) -> Callable:
        """
        Main application method for handling HTTP requests.

        Args:
            - `environ` (dict): The WSGI environment dictionary.
            - `start_response` (Callable): The callable for starting the response.

        Returns:
            `Callable`: The response callable.
        """

        request = Request(environ)
        urls = url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
            response = endpoint(request, *args)
        except HTTPException as e:
            response = e
            logger.error(
                f"Endpoint: {request.path}, Method: {request.method}, Response Status: {e}")
        return response(environ, start_response)

    def run(self) -> None:
        """
        Start the server and listen for incoming requests.

        Raises:
            - `SystemExit`: If an exception occurs while starting the server.

        Returns:
            `None`        
        """

        try:
            run_simple("127.0.0.1", 4000, self.application)
        except Exception as e:
            logger.error("Unable to start server", e)
            return sys.exit(1)
