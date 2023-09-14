import re


def snake_case(input_str):
    # Check if the input string is in snake case
    if re.match(r'^[a-z_]+$', input_str):
        return input_str  # Already in snake case, no correction needed

    # Replace spaces and capitalize letters with underscores
    snake_case_str = re.sub(
        r'[\sA-Z]', lambda x: '_' + x.group(0).lower(), input_str)

    # Remove leading underscores
    snake_case_str = snake_case_str.lstrip('_')

    return snake_case_str
