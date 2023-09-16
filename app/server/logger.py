from app.logger.logger import FORMATTER, LOG_LEVELS, setup_logger
from config.app import Config
import logging
import coloredlogs


def setup_werkzeug_logger(config: Config):
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


werkzeuf_logger = setup_werkzeug_logger(Config)
logger = setup_logger(f"{Config.APP_NAME.lower()}.route", Config)
