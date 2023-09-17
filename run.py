
from app.config import Config
from app.logger import logger
from app.utils.importing import import_classes, import_model, import_route

logger.warning(f"Starting application {Config.APP_NAME}")


if Config.APP_DATABASE:
    import_classes(import_model, "model")

if Config.APP_SERVER:
    import_classes(import_route, "route")
    from app.server.server import run
    run()
