from medusa.controllers.controller import Controller
from medusa.server.decorator import merge_request
from medusa.utils.merge import merge


class IndexController(Controller):
    @classmethod
    @merge_request
    def index(cls, request, *args, **kwargs):

        return request
