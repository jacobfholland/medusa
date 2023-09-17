from medusa.logger import setup_logger

from .config import UtilsConfig as Config

# Create a logger instance
logger = setup_logger(f"{Config.APP_NAME.lower()}.utils", Config)
