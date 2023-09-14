from app.logger.logger import logger
from app.database.import_models import import_models
from app.server.werzeug import run
from app.utils.merge import merge


logger.warning("Starting application")


def database():
    from app.database.database import Database
    db = Database()
    import_models(db)
    # db.init_db()


database()
run()
