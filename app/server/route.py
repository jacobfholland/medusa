from utils.format import snake_case

from app.server.decorators import route
from app.server.logger import logger
from app.server.server import url_map


class Route:
    @classmethod
    def __url_prefix__(cls):
        return f"/{snake_case(cls.__name__)}"

    @classmethod
    def routes(self):
        pass
