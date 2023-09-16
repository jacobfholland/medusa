import re
import uuid


def snake_case(input_str):
    if re.match(r'^[a-z_]+$', input_str):
        return input_str
    snake_case_str = re.sub(
        r'[\sA-Z]', lambda x: '_' + x.group(0).lower(), input_str)
    snake_case_str = snake_case_str.lstrip('_')

    return snake_case_str


def generate_uuid() -> str:
    """
    Generate a unique identifier using uuid.

    Returns:
        str: Generated unique identifier.
    """

    return str(uuid.uuid4())
