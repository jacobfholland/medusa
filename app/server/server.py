import sys
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

from app.server.logger import logger

url_map = Map()


class Server:
    def application(self, environ, start_response):
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

    def run(self,):
        try:
            run_simple("127.0.0.1", 4000, self.application)
        except Exception as e:
            logger.error("Unable to start server", e)
            return sys.exit(1)
