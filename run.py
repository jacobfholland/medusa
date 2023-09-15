from config.app import Config
from app.logger.logger import logger
from app.database.import_models import import_models_routes
from app.server.werzeug import run
from app.utils.merge import merge


logger.warning("Starting application")


def database():
    from app.database.database import Database
    db = Database(import_models_routes())


database()
run()
