from medusa.logger import setup_logger
from medusa.utils.environment import log_env_vars

from .config import DatabaseConfig as Config

logger = setup_logger(f"{Config.APP_NAME.lower()}.database", Config)
"""Create a database logger instance"""

log_env_vars(Config, logger)
