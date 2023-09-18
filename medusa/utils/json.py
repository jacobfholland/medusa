from datetime import date, datetime, time
from typing import Union


def serializer(obj: Union[datetime, date, time]) -> str:
    """Serialize datetime, date, or time objects into string representations.

    Args:
        - `obj` (Union[datetime, date, time]): The object to be serialized.

    Raises:
        - `TypeError`: If the input object is not a supported type for serialization.

    Returns:
        `str`: The serialized string representation of the input object.
    """

    if isinstance(obj, (datetime, date, time)):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
    raise TypeError(f"Type {type(obj)} not serializable")
