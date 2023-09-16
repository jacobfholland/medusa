# from .config import DatabaseConfig
from app.logger.logger import setup_logger
from config.app import Config

# Create the database logger
logger = setup_logger(f"{Config.APP_NAME.lower()}.route", Config)
