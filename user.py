from app.database.model import Model
from werkzeug.wrappers import Response
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from app.logger.logger import logger


class User(Model):
    def register_routes(self):
        self.url_map.add(Rule('/hello', endpoint=self.hello))
        self.url_map.add(Rule('/world', endpoint=self.world))

    def hello(self, request):
        logger.debug(
            f"Endpoint: /hello, Method: {request.method}, Response Status: 200")
        return Response("Hello, World!")

    def world(self, request):
        logger.debug(
            f"Endpoint: /world, Method: {request.method}, Response Status: 200")
        return Response("World, Hello!")
