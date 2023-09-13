from .config import DatabaseConfig
from config.app import Config
from app.logger.logger import setup_logger

# Create the database logger
logger = setup_logger(f"{Config.APP_NAME.lower()}.database", DatabaseConfig)
