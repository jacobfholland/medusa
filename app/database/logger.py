from app.logger import setup_logger

from .config import DatabaseConfig as Config


# Create a logger instance
logger = setup_logger(f"{Config.APP_NAME.lower()}.database", Config)
