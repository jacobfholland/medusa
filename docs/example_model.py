from medusa.config import Config
from medusa.database.model import Model
from medusa.utils.decorator import require_envs


example_variable = "A loose variable outside of a function or class"
"""Relevant information about this variable."""


class ExampleModel(Model):
    """A short and easy to understand description of the class.

    Sometimes they can span across multiple lines. Try and keep the lines under 80 characters.
    Your descriptions should make it clear what your code does for the next person working on it.

    Notes:
        - Any notes that may be relevant. Often used for quick implementation information.

    Inherits:
        - `Model`: A parent model class used for database functionality

    Attributes:
        - `attr1` (bool): A true or false attribute.
        - `attr2` (int): An integer attribute.
        - `attr3` (str): A string attribute.
        - `attr4` (SomeClass): An object attribute.
        - `attr5` (float): A float attribute, assigned during initilization.

    Methods:
        - `example_method`: A class method example
    """

    __abstract__ = True  # Avoids creating a database table
    attr1 = True
    attr2 = 50
    attr3 = "Example string"
    attr4 = Model

    def __init__(self) -> None:
        """Initializes a new instance of the Example class.

        Returns:
            `None`
        """
        self.attr5 = 123.45
        super().__init__()

    @require_envs(Config, ["ENV_VAR1", "ENV_VAR2"])
    def example_method(self, foo: dict, bar: str = None) -> int:
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

        Environment Variables:
            - `ENV_VAR1`: An environment variable set in the `.env` file.
            - `ENV_VAR2`: An different environment variable set in the `.env` file.

        Returns:
            `list`: A list of the input data.
        """

        try:
            # Inline comments are helpful to explain non-obvious bits of code
            bar += 1
            bar -= 1
            bar = 5
            if bar == 5:
                print(foo[bar])  # Prints the value of bar
        except KeyError as e:
            print(f"Failed to print the dictionary key: {e}")
        except Exception as e:
            print(f"Failed in some very unexpected way: {e}")
        return [foo, bar]
