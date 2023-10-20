import os

from dotenv import load_dotenv


def strip(input: str) -> str:
    """Strip the last two components from a file path.

    Args:
        - ``input`` (str): Input file path.

    Returns:
        ``str``: File path with the last two components removed.
    """

    return "/".join(input.split("/")[:-2])


def load_envs(directory: str) -> None:
    """Load environment variables from .env files found in the specified directory and its subdirectories.

    Args:
        - ``directory`` (str): The directory where .env files should be searched and loaded from.

    Returns:
        ``None``: Void.
    """

    for root, _, files in os.walk(directory):
        for file in files:
            if ".env" in file:
                env_file_path = os.path.join(root, file)
                load_dotenv(env_file_path)


FILE_DIRECTORY = os.path.abspath(__file__)
APP_DIR = strip(FILE_DIRECTORY)

# Load environment variables
load_envs(APP_DIR)


class Config:
    """Configuration class for the application.

    Attributes:
        - ``APP_NAME`` (str): The name of the application obtained from the environment 
          variables.
        - ``APP_DIR`` (str): The application's directory path.
        - ``LOG_LEVEL`` (str): The log level for the application obtained from the 
          environment variables.
        - ``LOG_PATH`` (str): The path where log files should be stored obtained from 
          the environment variables.
    """

    APP_NAME = os.environ.get("APP_NAME")
    APP_DIR = APP_DIR
    APP_DATABASE = eval(os.environ.get("APP_DATABASE", "False"))
    APP_SERVER = eval(os.environ.get("APP_SERVER", "False"))
    APP_MASK = eval(os.environ.get("APP_MASK", "False"))

    LOG_LEVEL = os.environ.get("LOG_LEVEL").upper()
    LOG_PATH = os.environ.get("LOG_PATH")
