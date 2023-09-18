
from medusa.config import Config
from medusa.logger import logger
from medusa.utils.importing import import_classes, import_model, import_route


def run() -> None:
    """Run the Medusa Application.

    This function starts the application based on the configuration in the object. 
    It enables or disables the database and server components based on the 
    environment variables.

    Raises:
        - `ImportError`: If the server package is missing.
        - `Exception`: If an unexpected error occurs while starting the server.

    Returns:
        `None`
    """

    logger.warning(f"Starting {Config.APP_NAME} application")
    if Config.APP_DATABASE:
        logger.info(f"Application database enabled")
        import_classes(import_model, "model")
    else:
        logger.warning(f"Application database disabled")
    if Config.APP_SERVER:
        logger.info(f"Application server enabled")
        try:
            from medusa.server.server import Server
            import_classes(import_route, "route")
            Server().run()
        except ImportError:
            logger.warning("Failed to start server - Server package missing")
        except Exception as e:
            logger.warning(f"Failed to start server - {e}")
    else:
        logger.warning(f"Application server disabled")
    logger.warning(f"Stopping application {Config.APP_NAME}")
