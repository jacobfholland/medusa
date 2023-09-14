import logging

import coloredlogs

from config.app import Config

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR
}
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def setup_logger(name: str, config: Config) -> logging.Logger:
    """
    Set up a logger with the given name and configuration.

    Args:
        name (str): The name of the logger.
        config (Config): An instance of the Config class containing logging settings.

    Returns:
        logging.Logger: A configured logger instance.
    """

    # Set up a logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    # Add colored handler for console output
    coloredlogs.install(level=config.LOG_LEVEL, logger=logger)

    # Create a FileHandler for logging to a file
    file_handler = logging.FileHandler(f"{config.LOG_PATH}/{name.lower()}.log")
    file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    app_file_handler = logging.FileHandler(
        f"{config.LOG_PATH}/{config.APP_NAME.lower()}.log")
    app_file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    file_handler.setFormatter(FORMATTER)
    app_file_handler.setFormatter(FORMATTER)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(app_file_handler)

    return logger


def setup_werkzeug_logger(config: Config):
    werkzeug_logger = logging.getLogger('werkzeug')

    # Clear existing handlers to avoid duplication
    werkzeug_logger.handlers.clear()

    # Set the log level
    werkzeug_logger.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))

    # Install coloredlogs first
    coloredlogs.install(fmt='[%(asctime)s] %(name)s %(levelname)s %(message)s',
                        level=config.LOG_LEVEL, logger=werkzeug_logger)

    # Create a FileHandler for logging to a file
    file_handler = logging.FileHandler(
        f"{config.LOG_PATH}/{config.APP_NAME.lower()}.werkzeug.log")
    file_handler.setLevel(LOG_LEVELS.get(config.LOG_LEVEL))
    file_handler.setFormatter(FORMATTER)

    # Add the FileHandler
    werkzeug_logger.addHandler(file_handler)
    werkzeug_logger.name = f"{Config.APP_NAME.lower()}.werkzeug"

    # Now manually set the formatter for all handlers (coloredlogs included)


setup_werkzeug_logger(Config)
logger = setup_logger(f"{Config.APP_NAME.lower()}.app", Config)
