import functools
from app.database.base import Base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.utils.utils import generate_uuid
from app.server.werzeug import url_map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
import json


def route(rule, methods=['GET']):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)

            # If it's already a Response object, return it as-is
            if isinstance(result, Response):
                return result

            # Check if result looks like HTML (rudimentary check)
            if isinstance(result, str) and result.strip().startswith("<"):
                return Response(result, content_type='text/html; charset=utf-8')

            # Default to JSON for other Python data types (dicts, lists, etc.)
            return Response(json.dumps(result), content_type='application/json; charset=utf-8')

        if not any([rule == r.rule for r in url_map.iter_rules()]):
            url_map.add(Rule(rule, endpoint=wrapped, methods=methods))

        return wrapped

    return decorator


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
        self.prefix = f"/{self.__class__.__name__.lower()}"
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

    def register_route(self, endpoint):

        self.url_map.add(
            Rule(f'{self.prefix}/{endpoint}', endpoint=self.hello, methods=['POST']))

    @classmethod
    def register_crud(cls):
        cls.create()

    @classmethod
    @route(f"/user/create", methods=['GET'])
    def create(cls):
        return "<html>OK<html>"

    def register_routes(self):
        raise NotImplementedError(
            "This method should be overridden by subclass"
        )
