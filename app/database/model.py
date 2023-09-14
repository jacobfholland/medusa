from app.database.base import Base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.route.decorators import route
from app.route.route import Route
from app.utils.format import snake_case
from app.utils.utils import generate_uuid


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

    def register_crud(self):
        @route(self, "/create", methods=["POST"])
        def create(request):
            return "<html>OK<html>"

        @route(self, "/get", methods=["GET"])
        def get(request):
            return "<html>OK<html>"

        @route(self, "/update", methods=["PUT", "PATCH"])
        def update(request):
            return "<html>OK<html>"

        @route(self, "/delete", methods=["DELETE"])
        def delete(request):
            return "<html>OK<html>"
