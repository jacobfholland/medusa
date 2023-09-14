from app.database.logger import logger
from app.utils.printable import Printable
from app.utils.utils import require_envs
from .config import DatabaseConfig as Config
from sqlalchemy.exc import ArgumentError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
import sys
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.engine.base import Engine
import sys


class Database(Printable):
    """Singleton class that handles the database connection and session creation using SQLAlchemy.
    All models and attributes are bound during initialization.

    Attributes:
        _instance (bool): Used to determine if the database has previously been instantiated.
        _all_models (list): All models that were imported during initialization.
        uri (str): A string representing the full database connection URI.
        engine (Engine): SQLAlchemy Engine object responsible for executing queries.
        db (scoped_session): A SQLAlchemy scoped session object to manage individual sessions.
        base (DeclarativeMeta): The SQLAlchemy declarative base object for model creation.
    """

    _instance = None

    def __init__(self, models: list = []) -> None:
        """Initializes the database connection and creates tables for models.

        Args:
            models (dict, optional): A dictionary of model classes to be created.

        Notes:
            Initializes the SQLAlchemy engine, creates scoped sessions, and initiates tables.
        """

        logger.info("Initializing database")
        self.uri = self.generate_uri()
        self.engine = self.generate_engine()
        self.db = self.generate_database()
        self.base = self.generate_base()
        self.bind_models(models)
        self.base.metadata.create_all(bind=self.engine)
        logger.debug(self.__str__())
        logger.info("Database initialization complete")

    def bind_models(self, models: dict) -> None:
        for model in models:
            model.metadata.create_all(self.engine)

    def database_type(self, db_type: str) -> str:
        """Determines the database type based on the provided string and returns the appropriate connection URI.

        Args:
            db_type (str): A string representing the database type (e.g., "sqlite", "mysql").

        Returns:
            str: Connection URI for the specified database type.

        Raises:
            SystemExit: If the database type is unrecognized.
        """

        if db_type == "sqlite":
            return self.sqlite()
        elif db_type in ["mysql", "postgresql", "oracle", "mssql+pyodbc"]:
            return self.standard()
        logger.error("Unable to determine database type")
        return sys.exit(1)

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_NAME"])
    def sqlite(self) -> str:
        """Generates the SQLite connection URI using environment variables.

        Returns:
            str: The SQLite database connection URI.

        Environment Variables:
            DATABASE_PATH (str, optional): Optional storage path for the database
            DATABASE_TYPE (str): The type of the database
            DATABASE_NAME (str): The name of the database
        """

        if Config.DATABASE_PATH:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_PATH}/{Config.DATABASE_NAME}.db"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_NAME}.db"

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_HOSTNAME", "DATABASE_NAME", "DATABASE_PORT"])
    def standard(self) -> str:
        """Generates the standard connection URI for databases like MySQL, PostgreSQL, Oracle, etc.

        Returns:
            str: The standard database connection URI.

        Environment Variables:
            DATABASE_USER (str, optional): The database user credential
            DATABASE_PASSWORD (str, optional): The database password credential
            DATABASE_HOSTNAME (str): The database hostname
            DATABASE_PORT (int): The database connection port
            DATABASE_TYPE (str): The type of the database
            DATABASE_NAME (str): The name of the database
        """

        if Config.DATABASE_USER and Config.DATABASE_PASSWORD:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOSTNAME}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_HOSTNAME}/{Config.DATABASE_NAME}"

    @require_envs(Config, ["DATABASE_TYPE"])
    def generate_uri(self) -> str:
        """Constructs the database URI by calling the appropriate URI generation method based on the database type.

        Returns:
            str: The database connection URI.
        Environment Variables:
            DATABASE_TYPE (str): The type of the database
        """

        uri = self.database_type(Config.DATABASE_TYPE)
        logger.debug(f"Generated database URI: {uri}")
        return uri

    def generate_engine(self) -> Engine:
        """Creates an SQLAlchemy Engine for query execution.

        Returns:
            Engine: An SQLAlchemy Engine object.

        Raises:
            ArgumentError: If the URI for database connection is malformed.
            SystemExit: For generic exceptions that cause engine creation to fail.
        """

        try:
            engine = create_engine(self.uri)
            logger.debug("Database engine created")
            return engine
        except ArgumentError:
            logger.error(
                "Failed to create database engine due to malformed database URI")
            return sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            return sys.exit(1)

    def generate_database(self) -> scoped_session:
        """Creates and returns a scoped session for transaction management.

        Returns:
            scoped_session: A SQLAlchemy scoped_session object.

        Raises:
            SystemExit: If an exception occurs during the creation of the scoped session.
        """

        try:
            db = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine,
                )
            )
            logger.debug("Scoped session created")
            return db
        except Exception as e:
            logger.error(f"Failed to screate scoped session: {e}")
            return sys.exit(1)

    def generate_base(self) -> DeclarativeMeta:
        """Generates the SQLAlchemy declarative base for defining models.

        Returns:
            DeclarativeMeta: The SQLAlchemy declarative base.

        Raises:
            SystemExit: If an exception occurs while creating the declarative base.
        """

        try:
            base = declarative_base()
            base.query = self.db.query_property()
            logger.debug("SQLAlchemy declarative base and query created")
            return base
        except Exception as e:
            logger.error(f"Failed to connect to {self.uri}: {e}")
            return sys.exit(1)