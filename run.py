
from app.config import Config
from app.database.importing import import_models
from app.server.importing import import_routes
from app.logger import logger
from app.server.server import run

logger.warning(f"Starting application {Config.APP_NAME}")


if Config.APP_DATABASE:
    import_models()

if Config.APP_SERVER:
    import_routes()
    run()
