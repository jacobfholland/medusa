from app.logger import setup_logger

from .config import DatabaseConfig


# Create a logger instance using the setup_logger function.
logger = setup_logger(
    f"{DatabaseConfig.APP_NAME.lower()}.database", DatabaseConfig
)
