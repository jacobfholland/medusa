from app.database.model import Model
from werkzeug.wrappers import Response
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from app.logger.logger import logger


class User(Model):
    __url_prefix__ = "/user"
