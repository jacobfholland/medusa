
from app.database.importing import import_models, import_routes
from app.logger.logger import logger
from config.app import Config

from app.server.server import run


logger.warning(f"Starting application {Config.APP_NAME}")

import_routes()
import_models()

if Config.APP_SERVER:
    run()
