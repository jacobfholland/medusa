from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr

# Uses absolute paths for auto-import functionality
from app.database.base import Base, Engine
from app.database.logger import logger
from app.utils.format import generate_uuid, snake_case

# Attempt to utilize the Server package for registering CRUD routes
try:
    from app.server.route import Route
except ImportError:
    from app.utils.dummy import DummyRoute as Route


class Model(Route, Base):
    """An abstract base class for all SQLAlchemy models in this project. 
    Contains common fields that are expected to be in all derived models.
    """

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    uuid = Column(String, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @classmethod
    def register_model(cls):
        try:
            cls.metadata.create_all(Engine)
            logger.debug(
                f"Synced {cls.__name__} database table {snake_case(cls.__name__)}"
            )
        except Exception as e:
            logger.error(
                f"Unable to generate database table for {cls.__name__}"
            )
        if not cls.__name__ == "Model":
            cls.routes()

    def __init__(self):
        super().__init__()

    @declared_attr
    def __tablename__(cls) -> str:
        """
        The database table name for the model. Detected by SQLAlchemy.

        Returns:
            str: The table name for the model, derived from the class name.
        """

        return snake_case(cls.__name__)

    @declared_attr
    def __table_args__(cls) -> dict:
        """
        Sets SQLAlchemy to extend a table that already exists instead of trying
        to recreate it.

        Returns:
            dict: Argument to extend existing tables (value Boolean)
        """

        return {'extend_existing': True}

    @classmethod
    def routes(cls):
        try:
            from app.server.decorator import route

            @route(cls, "/create", methods=["POST"])
            def create(request):
                return "<html>OK<html>"

            @route(cls, "/get", methods=["GET"])
            def get(request):
                return "<html>MODEL GET<html>"

            @route(cls, "/update", methods=["PUT", "PATCH"])
            def update(request):
                return "<html>OK<html>"

            @route(cls, "/delete", methods=["DELETE"])
            def delete(request):
                return "<html>OK<html>"
        except ImportError:
            pass
        return True
