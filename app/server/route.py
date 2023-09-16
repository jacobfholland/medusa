from .decorators import route
from .server import url_map
from app.utils.format import snake_case

from .logger import logger


class Route:
    def __init__(self):
        self.url_map = url_map
        try:
            self.routes()
        except Exception as e:
            logger.error(
                f"Failed to register CRUD routes for {self.__class__.__name__}: {e}")

    @property
    def __url_prefix__(self):
        return f"/{snake_case(self.__class__.__name__)}"

    def routes(self):
        pass
