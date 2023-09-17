from app.config import Config
from app.logger import setup_logger

logger = setup_logger(f"{Config.APP_NAME.lower()}.utils", Config)