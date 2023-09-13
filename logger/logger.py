import logging

import coloredlogs

from config.app import Config


def setup_logger(name: str, config: Config) -> logging.Logger:
    """
    Set up a logger with the given name and configuration.

    Args:
        name (str): The name of the logger.
        config (Config): An instance of the Config class containing logging settings.

    Returns:
        logging.Logger: A configured logger instance.
    """

    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR
    }
    # Set up a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_levels.get(config.LOG_LEVEL))

    # Add colored handler for console output
    coloredlogs.install(level=config.LOG_LEVEL, logger=logger)

    # Create a FileHandler for logging to a file
    file_handler = logging.FileHandler(f"{config.LOG_PATH}/{name.lower()}.log")
    file_handler.setLevel(log_levels.get(config.LOG_LEVEL))

    app_file_handler = logging.FileHandler(
        f"{config.LOG_PATH}/{config.APP_NAME.lower()}.log")
    app_file_handler.setLevel(log_levels.get(config.LOG_LEVEL))

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    app_file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(app_file_handler)

    return logger


logger = setup_logger(f"{Config.APP_NAME.lower()}.app", Config)
