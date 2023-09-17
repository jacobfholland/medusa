from .config import UtilsConfig as Config

from app.logger import setup_logger


# Create a logger instance
logger = setup_logger(f"{Config.APP_NAME.lower()}.utils", Config)
