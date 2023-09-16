from app.config import Config
from app.logger import setup_logger

from .config import DatabaseConfig

logger = setup_logger(f"{Config.APP_NAME.lower()}.database", DatabaseConfig)
