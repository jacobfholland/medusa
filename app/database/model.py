from app.database.base import Base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.utils.utils import generate_uuid
from app.server.werzeug import url_map
from werkzeug.routing import Rule


class Model(Base):
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

    def __init__(self):
        self.url_map = url_map
        self.register_crud()
        self.register_routes()

    @declared_attr
    def __tablename__(cls) -> str:
        """
        The database table name for the model. Detected by SQLAlchemy.

        Returns:
            str: The table name for the model, derived from the class name.
        """

        return cls.__name__.lower()

    @declared_attr
    def __table_args__(cls) -> dict:
        """
        Sets SQLAlchemy to extend a table that already exists instead of trying
        to recreate it.

        Returns:
            dict: Argument to extend existing tables (value Boolean)
        """

        return {'extend_existing': True}

    def register_crud(self):
        self.url_map.add(Rule('/create', endpoint=self.hello))
        self.url_map.add(Rule('/get', endpoint=self.world))
        self.url_map.add(Rule('/update', endpoint=self.world))
        self.url_map.add(Rule('/delete', endpoint=self.world))

    def register_routes(self):
        raise NotImplementedError(
            "This method should be overridden by subclass"
        )
