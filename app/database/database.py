import sys

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.scoping import scoped_session

# Uses absolute paths for auto-import functionality
from app.database.config import DatabaseConfig as Config
from app.database.logger import logger
from app.utils.decorator import require_envs


class Database:
    """Represents the database configuration and initialization.

    This class is responsible for initializing the database engine, database object,
    and SQLAlchemy base for working with database models.

    Attributes:
        uri (str): The database URI used for connection.
        engine (Engine): The SQLAlchemy engine for database communication.
        db (Session): The database session for interacting with the database.
        base (Base): The SQLAlchemy base class for defining database models.
    """

    def __init__(self) -> None:
        """Initialize the Database instance.

        This method sets up the database URI, engine, session, and base for database operations.

        Raises:
            Exception: If there's an issue during database initialization.
        """

        logger.info("Initializing database")
        self.uri = self.generate_uri()
        self.engine = self.generate_engine(self.uri)
        self.db = self.generate_database(self.engine)
        self.base = self.generate_base(self.uri, self.db)
        logger.info("Database initialization completed")

    @require_envs(Config, ["DATABASE_TYPE"])
    def generate_uri(self) -> str:
        """Constructs the database URI by calling the appropriate URI generation method based on the database type.

        Requires valid environment variables

        Returns:
            str: The database connection URI.

        Environment Variables:
            DATABASE_TYPE (str): The type of the database
        """

        uri = self.database_type(Config.DATABASE_TYPE)
        logger.debug(f"Generated database URI: {uri}")
        return uri

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
        elif db_type == "memory":
            return self.memory()
        elif db_type in ["mysql", "postgresql", "oracle", "mssql+pymssql", "firebird"]:
            return self.standard()
        logger.error("Unable to determine database type")
        return sys.exit(1)

    @require_envs(Config, ["DATABASE_TYPE"])
    def memory(self) -> str:
        """Create an SQLite in-memory database URI. Useful for unit testing.

        Returns:
            str: The SQLite in-memory database URI.
        """

        logger.debug(f"Database type {Config.DATABASE_TYPE}")
        return "sqlite:///:memory:"

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_NAME"])
    def sqlite(self) -> str:
        """Generates the SQLite connection URI using environment variables.

        Requires valid environment variables

        Returns:
            str: The SQLite database connection URI.

        Environment Variables:
            DATABASE_PATH (str, optional): Optional storage path for the database
            DATABASE_TYPE (str): The type of the database
            DATABASE_NAME (str): The name of the database
        """

        logger.debug(f"Database type {Config.DATABASE_TYPE}")
        if Config.DATABASE_PATH:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_PATH}/{Config.DATABASE_NAME}.db"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_NAME}.db"

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_HOSTNAME", "DATABASE_NAME", "DATABASE_PORT"])
    def standard(self) -> str:
        """Generates the standard connection URI for databases like MySQL, PostgreSQL, Oracle, etc.

        Requires valid environment variables

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

        logger.debug(f"Database type {Config.DATABASE_TYPE}")
        if Config.DATABASE_USER and Config.DATABASE_PASSWORD:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOSTNAME}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_HOSTNAME}/{Config.DATABASE_NAME}"

    def generate_engine(self, uri) -> Engine:
        """Creates an SQLAlchemy Engine for query execution.

        Returns:
            Engine: An SQLAlchemy Engine object.

        Raises:
            ArgumentError: If the URI for database connection is malformed.
            SystemExit: For generic exceptions that cause engine creation to fail.
        """

        try:
            engine = create_engine(uri)
            logger.debug("Database engine created")
            return engine
        except ArgumentError:
            logger.error(
                "Failed to create database engine due to malformed database URI")
            return sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            return sys.exit(1)

    def generate_database(self, engine) -> scoped_session:
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
                    bind=engine,
                )
            )
            logger.debug("Scoped session created")
            return db
        except Exception as e:
            logger.error(f"Failed to screate scoped session: {e}")
            return sys.exit(1)

    def generate_base(self, uri, db) -> DeclarativeMeta:
        """Generates the SQLAlchemy declarative base for defining models.

        Returns:
            DeclarativeMeta: The SQLAlchemy declarative base.

        Raises:
            SystemExit: If an exception occurs while creating the declarative base.
        """

        try:
            base = declarative_base()
            base.query = db.query_property()
            logger.debug("SQLAlchemy declarative base and query created")
            return base
        except Exception as e:
            logger.error(f"Failed to connect to {uri}: {e}")
            return sys.exit(1)
