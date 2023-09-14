from app.server.werzeug import url_map
from sqlalchemy.ext.declarative import declared_attr


class Route:
    def __init__(self):
        self.url_map = url_map
        super().__init__()
