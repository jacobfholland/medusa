from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

from .logger import logger

url_map = Map()


def application(environ, start_response):
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


def run():
    run_simple("127.0.0.1", 4000, application)
