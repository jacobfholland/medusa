from medusa.controllers.controller import Controller


class IndexController(Controller):
    @classmethod
    def index(cls, request):
        # TODO: Decorators to test for various validation or permissions
        # print(vars(request))
        return request
