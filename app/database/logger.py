from app.logger import setup_logger

from .config import DatabaseConfig

logger = setup_logger(
    f"{DatabaseConfig.APP_NAME.lower()}.database", DatabaseConfig
)
