import logging
import os

import coloredlogs

from medusa.config import Config

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR
}
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def setup_logger(name: str, config: Config) -> logging.Logger:
    """Set up a logger with the given name and configuration.

    Args:
        - ``name`` (str): The name of the logger.
        - ``config`` (`Config`): An instance of the Config class containing logging settings.

    Returns:
        ``Logger``: A configured logger instance.
    """

    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    coloredlogs.install(level=config.LOG_LEVEL, logger=logger)

    file_handler = logging.FileHandler(f"{config.LOG_PATH}/{name.lower()}.log")
    file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    app_file_handler = logging.FileHandler(
        f"{config.LOG_PATH}/{config.APP_NAME.lower()}.log")
    app_file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    file_handler.setFormatter(FORMATTER)
    app_file_handler.setFormatter(FORMATTER)

    logger.addHandler(file_handler)
    logger.addHandler(app_file_handler)

    return logger


logger = setup_logger(f"{Config.APP_NAME.lower()}.app", Config)
"""Create an app logger instance"""
