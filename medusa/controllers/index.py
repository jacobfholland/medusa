from medusa.controllers.controller import Controller


class IndexController(Controller):
    @classmethod
    def index(cls, request=None):
        return f"""
        <h1>Index Page</h1>
        <br>
        {request}
        """
