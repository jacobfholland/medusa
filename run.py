
from app.database.importing import import_models, import_routes
from app.logger.logger import logger
from app.server.server import run
from config.app import Config

logger.warning(f"Starting application {Config.APP_NAME}")


if Config.APP_DATABASE:
    import_models()

if Config.APP_SERVER:
    import_routes()
    run()
