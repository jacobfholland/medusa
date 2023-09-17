
from medusa.config import Config
from medusa.logger import logger
from medusa.utils.importing import import_classes, import_model, import_route


def run() -> None:
    """Run the Medusa application.

    This function starts the application based on the configuration in the
    Config object. It enables or disables the database and server components
    based on the environment variables.

    Returns:
        None
    """

    logger.warning(f"Starting {Config.APP_NAME} application")
    if Config.APP_DATABASE:
        logger.info(f"Application database enabled")
        import_classes(import_model, "model")
    else:
        logger.warning(f"Application database disabled")
    if Config.APP_SERVER:
        logger.info(f"Application server enabled")
        import_classes(import_route, "route")
        from medusa.server.server import Server
        Server().run()
    else:
        logger.warning(f"Application server disabled")
    logger.warning(f"Stopping application {Config.APP_NAME}")
