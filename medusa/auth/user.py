from typing import Callable

from medusa.auth.route import UserRoute
from medusa.database.decorator import attribute
from medusa.database.model import Model
from medusa.server.decorator import route
from medusa.utils.format import snake_case


class User(Model):
    """User model in the application.

    This class inherits from the `Model` base class, which provides common fields 
    and functionality for database models. It is used to define and interact with 
    user data in the database.

    Methods:
        - ``routes``: Define custom User routes.
    """

    route = UserRoute
