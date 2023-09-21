import logging
import os

import coloredlogs

from medusa.logger import FORMATTER, LOG_LEVELS, setup_logger

from .config import ServerConfig as Config


def setup_werkzeug_logger(config: Config) -> None:
    """Set up the Werkzeug logger for the server. The Werkzeug logger already exists, so it intercepts the logger
    and replaces it with a custom logger.

    Args:
        - ``config`` (``Config``): The server configuration object.

    Returns:
        ``None``: Void.
    """

    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.handlers.clear()
    werkzeug_logger.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    coloredlogs.install(
        level=config.LOG_LEVEL,
        logger=werkzeug_logger
    )

    file_handler = logging.FileHandler(
        f"{config.LOG_PATH}/{config.APP_NAME.lower()}.werkzeug.log")
    file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))
    file_handler.setFormatter(FORMATTER)

    werkzeug_logger.addHandler(file_handler)
    werkzeug_logger.name = f"{Config.APP_NAME.lower()}.werkzeug"


# Intercepts and sets up the werkzeug logger
werkzeug_logger = setup_werkzeug_logger(Config)
"""Create a Werkzeug logger instance"""

logger = setup_logger(f"{Config.APP_NAME.lower()}.route", Config)
"""Create a server logger instance"""
