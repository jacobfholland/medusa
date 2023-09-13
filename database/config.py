import os

from config.app import Config


class DatabaseConfig(Config):
    """
    Configuration class for the database settings.

    This class inherits from the `Config` class and defines database-related
    configuration parameters using environment variables.

    Attributes:
        DATABASE_NAME (str): The name of the database.
        DATABASE_USER (str): The username for database authentication.
        DATABASE_PASSWORD (str): The password for database authentication.
        DATABASE_HOST (str): The host where the database server is located.
        DATABASE_PORT (str): The port on which the database server is listening.
        DATABASE_TYPE (str): The type or dialect of the database (e.g., 'mysql', 'postgresql').
        DATABASE_PATH (str): The path to the database file (if applicable).

    Note:
        All attribute values are obtained from corresponding environment variables.
    """

    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_TYPE = os.environ.get("DATABASE_TYPE")
    DATABASE_PATH = os.environ.get("DATABASE_PATH")
