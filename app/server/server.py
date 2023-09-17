import sys
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request
from app.server.logger import logger

# Application URL Map (registered endpointds)
url_map = Map()


class Server:
    def application(self, environ: dict, start_response: callable) -> callable:
        """
        Main application method for handling HTTP requests.

        Args:
            environ (dict): The WSGI environment dictionary.
            start_response (callable): The callable for starting the response.

        Returns:
            callable: The response callable.
        """

        request = Request(environ)
        urls = url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
            response = endpoint(request, **args)
        except HTTPException as e:
            response = e
            logger.error(
                f"Endpoint: {request.path}, Method: {request.method}, Response Status: {e}")

        return response(environ, start_response)

    def run(self) -> None:
        """
        Start the server and listen for incoming requests.

        Raises:
            SystemExit: If an exception occurs while starting the server.
        """

        try:
            run_simple("127.0.0.1", 4000, self.application)
        except Exception as e:
            logger.error("Unable to start server", e)
            return sys.exit(1)
