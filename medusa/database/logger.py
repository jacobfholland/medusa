from medusa.logger import setup_logger

from .config import DatabaseConfig as Config

logger = setup_logger(f"{Config.APP_NAME.lower()}.database", Config)
"""Create a database logger instance"""
