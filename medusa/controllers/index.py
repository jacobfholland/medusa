from medusa.controllers.controller import Controller


class IndexController(Controller):
    @classmethod
    def index(cls, request, *args, **kwargs):

        return request
