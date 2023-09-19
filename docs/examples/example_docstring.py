import os

from medusa.config import Config
from medusa.database.model import Model
from medusa.utils.decorator import require_envs


example_variable = "A variable outside of a function or class."
"""Relevant information about this variable."""


class ExampleDocstring(Model):
    """A short and easy to understand description of the class.

    Descriptions should be clear and may span multiple lines. Try to keep the
    lines under 80 characters.

    Notes:
        - Quick implementation notes may be relevant here.

    Inherits:
        - `Model`: Parent model class for database functionality.

    Args:
        - `*args`: Positional arguments for object creation.
        - `**kwargs`: Keyword arguments for object creation.

    Attributes:
        - `attr1` (bool): A true or false class attribute.
        - `attr2` (int): An integer class attribute.
        - `attr3` (str): A string class attribute.
        - `attr4` (Model): An object class attribute.
        - `attr5` (float, init): Float attribute, assigned during initialization.
        - `attr6` (str, property): Combines `attr2` and `attr3` as a computed value.

    Methods:
        - `example_method`: Example class method.
    """

    attr1 = True
    attr2 = "Lorem ipsum"
    attr3 = "Example string"
    attr4 = Model

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a new `Model` instance.

        Initialization should always return `None`.

        Args:
            - `*args`: Positional arguments for object creation.
            - `**kwargs`: Keyword arguments for object creation.
        """

        self.attr5 = 123.45
        super().__init__()

    @property
    def attr6(self) -> str:
        """Computed class attribute.

        Binds an attribute to a function for calculated assignment.

        Raises:
            - `KeyError`: Handles failed concatenation.
            - `Exception`: Catch-all for unexpected exceptions.

        Returns:
            - `str`: Concatenation of `attr2` and `attr3`.
        """

        try:
            output = self.attr2 + self.attr3
        except TypeError as e:
            return f"Failed to assign output value: {e}"
        except Exception as e:
            return f"Failed in some unexpected way: {e}"
        return output

    @require_envs(Config, ["ENV_VAR1", "ENV_VAR2"])
    def example_method(self, foo: dict, bar: str = None) -> list:
        """Short and easy to understand method description.

        Descriptions should be clear and may span multiple lines. Aim for lines
        under 80 characters.

        Notes:
            - Utilizes `@require_envs` requiring select environment variables.

        Args:
            - `foo` (dict): A dictionary input parameter.
            - `bar` (str, optional): An optional string parameter.

        Raises:
            - `KeyError`: Handles failed dictionary key access.
            - `Exception`: Catch-all for unexpected exceptions.

        Environment Variables (custom):
            - `ENV_VAR1`: Set in the `.env` file.
            - `ENV_VAR2`: Another variable set in the `.env` file.

        Returns:
            - `list`: A list of the input data.
        """

        try:
            # Inline comments are helpful to explain non-obvious bits of code
            if os.environ["BAR"] == bar:
                print(foo[bar])  # Prints the value of the `bar` key in `foo`
        except KeyError as e:
            return ["Failed to print the dictionary key", e]
        except Exception as e:
            return ["Failed in some unexpected way", e]
        return [foo, bar]
