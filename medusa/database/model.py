from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from medusa.controllers.controller import Controller

# Uses absolute paths for auto-import functionality
from medusa.database.base import Base
from medusa.database.config import DatabaseConfig as Config
from medusa.database.decorator import attribute
from medusa.database.logger import logger

from medusa.utils.format import generate_uuid, snake_case
from medusa.utils.merge import merge_request

# Attempt to use `Route` functionality if `Server` package is installed
# If package is missing, will use an empty class to not break the inheritance

from medusa.server.route import Route


class Model(Base):
    """An abstract base class for all SQLAlchemy models in this project.

    This class contains common fields that are expected to be present in all derived 
    models.

    Attributes:
        - ``id`` (Column): The primary key for the model.
        - ``uuid`` (Column): The UUID field for the model.
        - ``created_at`` (Column): The timestamp of creation.
        - ``updated_at`` (Column): The timestamp of the last update.

    Notes:
        - All method overrides should return `super`
        - Subclasses of `Model` should override the `create()` method to define 
          specific create behavior.
        - Subclasses of `Model` should override the `get()` method to define 
          specific get behavior.
        - Subclasses of `Model` should override the `update()` method to define 
          specific update behavior.
        - Subclasses of `Model` should override the `delete()` method to define 
          specific delete behavior.
    """

    __table_args__ = {'extend_existing': True}
    __abstract__ = True  # Ignores database table creation
    route = Route
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

    def __init__(self) -> None:
        """Initialize a new `Model` instance.

        Returns:
            ``None``: Void.
        """

        super().__init__()

    @attribute
    def controller(cls):
        return Controller

    @declared_attr
    def __tablename__(cls) -> str:
        """The database table name for the model.

        Table name is derived from the class name using snake_case.

        Returns:
            ``str``: The table name for the model.
        """

        return snake_case(cls.__name__)

    @classmethod
    def routes(cls, _class):
        return cls.route.routes(cls)
