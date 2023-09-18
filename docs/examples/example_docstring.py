import os

from medusa.config import Config
from medusa.database.model import Model
from medusa.utils.decorator import require_envs


example_variable = "A variable outside of a function or class."
"""Relevant information about this variable."""


class ExampleDocstring(Model):
    """A short and easy to understand description of the class.

    Sometimes they can span across multiple lines. Try and keep the lines under 80 characters.
    Your descriptions should make it clear what your code does for the next person working on it.

    Notes:
        - Any notes that may be relevant. Often used for quick implementation information.

    Inherits:
        - `Model`: A parent model class used for database functionality.

    Args:
        - `*args`: Positional arguments used when creating an object.
        - `*kwargs`: Key word arguments used when creating an object.

    Attributes:
        - `attr1` (bool): A true or false class attribute.
        - `attr2` (int): An integer class attribute.
        - `attr3` (str): A string class attribute.
        - `attr4` (Model): An object class attribute.
        - `attr5` (float): A float class attribute, assigned during initialization.
        - `attr6` (str): A computed value that combines `attr2` and `attr3`.

    Methods:
        - `example_method`: A class method example.
    """

    attr1 = True
    attr2 = "Lorem ipsum"
    attr3 = "Example string"
    attr4 = Model

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a new `Model` instance.

        Initialization class functions should always return `None`.

        Args:
            - `*args`: Positional arguments used when creating an object.
            - `*kargs`: Key word arguments used when creating an object.
        """

        self.attr5 = 123.45
        super().__init__()

    @property
    def attr6(self) -> str:
        """Computed class attribute

        This special method is used when you want to assign an attribute on a class that requires 
        calculation. It binds an attribute to a function.

        Raises:
            - `KeyError`: Gracefully handle failed concatenation.
            - `Exception`: Bare catch-all for any unexpected exceptions.

        Returns:
            - `str`: A concatenation of `attr2` and `attr3`.
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
        """A short and easy to understand description of the method.

        Sometimes they can span across multiple lines. Try and keep the lines under 80 characters.
        Your descriptions should make it clear what your code does for the next person working on it.

        Notes:
            - This function utilizes the `@require_envs` decorator, which requires select environment
            variables to be set.

        Args:
            - `foo` (dict): A dictionary input parameter.
            - `bar` (str, optional): An optional string parameter.

        Raises:
            - `KeyError`: Gracefully handle failed dictionary key access.
            - `Exception`: Bare catch-all for any unexpected exceptions.

        Environment Variables (custom):
            - `ENV_VAR1`: An environment variable set in the `.env` file.
            - `ENV_VAR2`: An different environment variable set in the `.env` file.

        Returns:
            `list`: A list of the input data.
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
