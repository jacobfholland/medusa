from app.database.model import Model
from app.server.decorator import route


class User(Model):
    def __init__(self):
        super().__init__()

    @classmethod
    def routes(cls):
        @route(cls, "/get", methods=["GET"])
        def get(request):
            return "<html>USER GET<html>"

        return super().routes()
