from app.logger.logger import setup_logger
from config.app import Config

from .config import DatabaseConfig

# Create the database logger
logger = setup_logger(f"{Config.APP_NAME.lower()}.database", DatabaseConfig)
