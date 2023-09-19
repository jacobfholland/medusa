from datetime import date, datetime, time
from typing import Any, Union

import werkzeug
from werkzeug.datastructures import EnvironHeaders

from .logger import logger


def delete_value(data: dict, key: str) -> None:
    """Delete a specific key-value pair from a dictionary.

    Attempts to remove a key from the dictionary. If the key is not found, logs 
    a debug message.

    Args:
        - `data` (dict): The dictionary from which the key-value pair will be deleted.
        - `key` (str): The key that needs to be deleted.

    Notes:
        - The function is primarily used during the serialization of Werkzeug's Request object.
    """
    try:
        del data["environ"][key]
    except KeyError as e:
        logger.debug(f"Key {key} not found on object during serilization")
        pass


def serializer(obj: Any) -> Union[str, dict, None]:
    """Custom JSON serializer function.

    This function is intended to serialize various types of objects into JSON-friendly
    formats. It turns datetime objects into string format and Werkzeug's Request 
    object into a simplified dictionary.

    Args:
        - `obj` (Any): The object that needs to be serialized.

    Raises:
        - `TypeError`: If the object type is not serializable.

    Returns:
        - `Union[str, dict, None]`: The serialized object. 
    """

    IGNORE_KEYS = [
        "wsgi.input",
        "wsgi.errors",
        "werkzeug.socket",
        "werkzeug.request"
    ]
    if isinstance(obj, (datetime, date, time)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, werkzeug.wrappers.Request):
        request_data = vars(obj)
        for key in IGNORE_KEYS:
            delete_value(request_data, key)
        return request_data
    if isinstance(obj, bytes):
        return None
    if isinstance(obj, EnvironHeaders):
        return dict(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
