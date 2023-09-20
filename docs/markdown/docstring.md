# Docstrings and Type Hinting
Adhering to a standardized set of guidelines for docstrings and type hinting ensures 
that the code remains readable, maintainable, and self-explanatory. Below are the 
standards expected for making docstrings.

**<span style="color: #dc3545;">IMPORTANT:</span>** Non-compliance with the guidelines 
for docstrings and type hinting laid out in this document will result in the rejection 
of pull requests.

## Example
```python
import os
from typing import List

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
    def example_method(self, foo: dict, bar: str = None) -> List[dict, str]:
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
```
## Rules
- All classes, methods, functions, and module variables must have a docstring.
- Docstring lines should ideally not exceed 80 characters.
- The general rule of thumb for formatting a section line is: 
`- 'key' (type): Lorem ipsum`
    - **(The single quotes are actually backticks. Markdown limits displaying 
    backticks on this page.)*
- Use a single line break between sections.
- References to data types, classes, functions, methods, etc. should use 
backticks to indicate a reference. This includes if an argument is a reference.
- Include periods at the end of sentences.

### Classes
Class docstrings must include one or more sections. **Description** 
is mandatory. They should appear in this order, if applicable. Only include 
applicable sections.


#### 1. Description:
```
"""Description text goes here

Second line of text goes here
"""
```
- Mandatory.
- Uses `"""`.
- Can be single or multiple lines.
- Text begins on the same line the comment begins on.
- If a single line, ending quotations stay on same line.
- Left aligned with the opening quotations.
- A line break between the description and sections

#### 2. Notes: *(if applicable)*
```
Notes:
    - Note about the class.
```
- Can have multiple notes.
- Usually for abnormal implementation hints.
- Each note is a single line only.

#### 3. Inherits: *(if applicable)*
```
Inherits:
    - `Class`: A parent class.
    - `OtherClass`: A second parent class.
```
- Can have multiple inherited classes.

#### 4. Args: *(if applicable)*
```
Args:
    - `example` (str): Example argument, defaults to "Hello".
    - `opt_arg` (int, optional): An optional argument.
```
- Can have multiple arguments.
- Include the data type.
- Mark any arguments optional as needed.
- Include a default value if there is one.
- If the argument is non-standard library object only include the
class name. Do not include the full module path. Note the full module
path in the `Notes` section

#### 5. Attributes: *(if applicable)*
```
Attributes:
    - `attr1` (str): Example class attribute.
    - `attr2` (int, @property): A computed class property.
    - `attr3` (bool, init): An attribute assigned during initialization.
```
- Can have multiple attributes.
- Include the data type.
- Mark any attributes assigned via *@property* or in the *init* function
as needed.

#### 6. Methods: *(if applicable)*
```
Methods:
    - `example_method`: Example class method.
    - `cls_method_example` (@classmethod): A class method that doesn't require an object.
```
- Can have multiple methods.
- Do not include the *init* or any other internal methods.
- Do not include parentheses *()*.
- Mark any methods created with *@classmethod* as needed.
#### 7. Custom: *(if applicable)*
```
Section (custom):
    - `value` (type, condition): A custom line that follows standard formatting.
```
- Only make a custom docstring section if it is absolutely necessary.
- It should be immediately obvious what your section is for and 
how to read it.
- Follow other rules as closely as possible.
- Include *(custom)* in the section name.

### Methods/Functions
Method and function docstrings must include one or more sections. **Description** 
and **Returns** are mandatory. They should appear in this order, if applicable. 
Only include applicable sections.

#### 1. Description:
```
"""Description text goes here.

Second line of text goes here.
"""
```
- Mandatory.
- Uses `"""`.
- Can be single or multiple lines.
- Text begins on the same line the comment begins on.
- If a single line, ending quotations stay on same line.
- Left aligned with the opening quotations.
- A line break between the description and sections

#### 2. Notes: *(if applicable)*
```
Notes:
    - Note about the class.
```
- Can have multiple notes.
- Usually for abnormal implementation hints.
- Each note is a single line only.

#### 3. Args: *(if applicable)*
```
Args:
    - `example` (str): Example argument, defaults to "Hello".
    - `opt_arg` (int, optional): An optional argument.
```
- Can have multiple arguments.
- Include the data type.
- Mark any arguments optional as needed.
- Include a default value if there is one.
- If the argument is non-standard library object only include the
class name. Do not include the full module path. Note the full module
path in the `Notes` section

#### 4. Raises: *(if applicable)*
```
Raises:
    - `Exception`: Catch-all for unexpected exceptions.
```
- Can have multiple exceptions.

#### 5. Custom: *(if applicable)*
```
Section (custom):
    - `value` (type, condition): A custom line that follows standard formatting.
```
- Only make a custom docstring section if it is absolutely necessary.
- It should be immediately obvious what your section is for and 
how to read it.
- Follow other rules as closely as possible.
- Include *(custom)* in the section name.

#### 6. Returns:
```
Returns:
    `List[str]`: Example list of strings.
```
- Can _not_ have multiple returns.
- Does not require a leading hypen.
- If returning *None* state if it is void or explicit.

### Module Variables
```
"""Description text goes here

Second line of text goes here
"""
```
- Mandatory.
- Uses `"""`.
- Can be single or multiple lines.
- Text begins on the same line the comment begins on.
- If a single line, ending quotations stay on same line.
- Left aligned with the opening quotations.

### Type Hinting
- Use Python >=3.5 compatible [type hinting](https://docs.python.org/3.8/library/typing.html).
- Include both argument and return type hints.