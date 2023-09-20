from medusa.logger import setup_logger

from .config import UtilsConfig as Config

logger = setup_logger(f"{Config.APP_NAME.lower()}.utils", Config)
"""Create a utils logger instance"""
