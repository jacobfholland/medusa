from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from app.database.base import Base, Engine
from app.database.config import DatabaseConfig as Config
from app.database.logger import logger
from app.utils.format import generate_uuid, snake_case

try:
    from app.server.route import Route
except ImportError:
    from app.utils.dummy import DummyRoute as Route


class Model(Route, Base):
    """An abstract base class for all SQLAlchemy models in this project.

    Contains common fields that are expected to be present in all derived models.
    """

    __abstract__ = True
    id = Column(Integer, primary_key=True, doc="Primary key for the model.")
    uuid = Column(
        String, default=generate_uuid,
        doc="UUID field for the model."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        doc="Timestamp of creation."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Timestamp of the last update."
    )

    @classmethod
    def register_model(cls) -> None:
        """Register the model with the database.

        Creates the database table for the model and sets up CRUD routes if the app server is enabled.

        Raises:
            Exception: If table creation fails.
        """

        try:
            cls.metadata.create_all(Engine)
            logger.debug(
                f"Synced {cls.__name__} database table {snake_case(cls.__name__)}"
            )
        except Exception as e:
            logger.error(
                f"Unable to generate database table for {cls.__name__}"
            )
        if not cls.__name__ == "Model" and Config.APP_SERVER:
            cls.routes()

    def __init__(self):
        super().__init__()

    @declared_attr
    def __tablename__(cls) -> str:
        """The database table name for the model.

        Table name is derived from the class name using snake_case.

        Returns:
            str: The table name for the model.
        """

        return snake_case(cls.__name__)

    @declared_attr
    def __table_args__(cls) -> dict:
        """Sets SQLAlchemy to extend an existing table instead of recreating it.

        Returns:
            dict: Arguments to extend existing tables (value Boolean).
        """

        return {'extend_existing': True}

    @classmethod
    def routes(cls) -> bool:
        """Define routes for the model.

        If the app server is enabled, this method defines routes for CRUD on model instances.

        Args:
            cls (type): The class associated with the routes. Must always be `cls`.

        Returns:
            super(): Parent `routes()` method
        """

        try:
            from app.server.decorator import route
            if Config.APP_SERVER:
                @route(cls, "/create", methods=["POST"])
                def create(request):
                    """Handler function for the create endpoint.

                    Args:
                        request (Request): The HTTP request object.

                    Returns:
                        Response: The HTTP response object.
                    """

                    return "<html>OK<html>"

                @route(cls, "/get", methods=["GET"])
                def get(request):
                    """Handler function for the get endpoint.

                    Args:
                        request (Request): The HTTP request object.

                    Returns:
                        Response: The HTTP response object.
                    """

                    return "<html>MODEL GET<html>"

                @route(cls, "/update", methods=["PUT", "PATCH"])
                def update(request):
                    """Handler function for the update endpoint.

                    Args:
                        request (Request): The HTTP request object.

                    Returns:
                        Response: The HTTP response object.
                    """

                    return "<html>OK<html>"

                @route(cls, "/delete", methods=["DELETE"])
                def delete(request):
                    """Handler function for the delete endpoint.

                    Args:
                        request (Request): The HTTP request object.

                    Returns:
                        Response: The HTTP response object.
                    """

                    return "<html>OK<html>"
        except ImportError:
            pass
        return super().routes()
