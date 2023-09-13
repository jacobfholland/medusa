from database.logger import logger
from utils.printable import Printable
from utils.utils import require_envs
from .config import DatabaseConfig as Config
from sqlalchemy.exc import ArgumentError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
import sys
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.engine.base import Engine
import ast
import importlib
import os
import sys
from pathlib import Path
import os
import glob
import importlib.util


class Database(Printable):
    """Handles database connection and session creation using SQLAlchemy.

    Attributes:
        uri: A string representing the database URI.
        engine: An SQLAlchemy Engine object.
        db: A scoped session object.
        base: The declarative base for SQLAlchemy models.
    """

    _instance = None

    def __init__(self):
        self.all_models = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.all_models = []
            cls._instance.init_db()
        return cls._instance

    def init_db(self, models: dict = None) -> None:
        """Initializes the Database class and sets up the database."""

        logger.info("Initializing database")
        self.uri = self.generate_uri()
        self.engine = self.generate_engine()
        self.db = self.generate_database()
        self.base = self.generate_base()
        if self.all_models:
            for model in self.all_models:
                model.metadata.create_all(self.engine)
        self.base.metadata.create_all(bind=self.engine)
        print(vars(self.base.metadata))
        logger.debug(self.__str__())
        logger.info("Database initialization complete")

    def database_type(self, db_type: str) -> str:
        """Determines the database type and returns the appropriate URL.

        Args:
            db_type: A string representing the type of the database.

        Returns:
            A string representing the appropriate database URL.
        """

        if db_type == "sqlite":
            return self.sqlite()
        elif db_type in ["mysql", "postgresql", "oracle", "mssql+pyodbc"]:
            return self.standard()
        logger.error("Unable to determine database type")
        return sys.exit(1)

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_NAME"])
    def sqlite(self) -> str:
        """Generates the SQLite database URL.

        Returns:
            A string representing the SQLite database URL.
        """

        if Config.DATABASE_PATH:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_PATH}/{Config.DATABASE_NAME}.db"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_NAME}.db"

    @require_envs(Config, ["DATABASE_TYPE", "DATABASE_HOST", "DATABASE_NAME", "DATABASE_PORT"])
    def standard(self) -> str:
        """Generates the standard (MySQL, PostgreSQL, Oracle, etc.) database URL.

        Returns:
            A string representing the standard database URL.
        """

        if Config.DATABASE_USER and Config.DATABASE_PASSWORD:
            return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOST}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"
        return f"{Config.DATABASE_TYPE}:///{Config.DATABASE_HOST}/{Config.DATABASE_NAME}"

    @require_envs(Config, ["DATABASE_TYPE"])
    def generate_uri(self) -> str:
        """Generates the database URL based on environment variables.

        Returns:
            A string representing the database URL.
        """

        uri = self.database_type(Config.DATABASE_TYPE)
        logger.debug(f"Generated database URI: {uri}")
        return uri

    def generate_engine(self) -> Engine:
        """Creates and returns an SQLAlchemy Engine.

        Returns:
            An SQLAlchemy Engine object.

        Raises:
            ArgumentError: If the database URI is malformed.
            Exception: For generic exceptions.
        """

        try:
            engine = create_engine(self.uri)
            logger.debug("Database engine created")
            return engine
        except ArgumentError:
            logger.error(
                "Failed to create database engine due to malformed database URI")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            sys.exit(1)

    def generate_database(self) -> scoped_session:
        """Creates and returns a scoped session.

        Returns:
            A scoped_session object.

        Raises:
            Exception: For generic exceptions.
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

    def generate_base(self) -> DeclarativeMeta:
        """Creates and returns an SQLAlchemy declarative base.

        Returns:
            A DeclarativeMeta object representing the SQLAlchemy declarative base.

        Raises:
            Exception: For generic exceptions.
        """

        try:
            base = declarative_base()
            base.query = self.db.query_property()
            logger.debug("SQLAlchemy declarative base and query created")
            return base
        except Exception as e:
            logger.error(f"Failed to connect to {self.uri}: {e}")
