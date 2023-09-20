import base64
from datetime import date, datetime, time
from typing import Any, Dict, Union

from werkzeug.datastructures import EnvironHeaders
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.wrappers import Request

from .logger import logger

IGNORE_KEYS = [
    "wsgi.input",
    "wsgi.errors",
    "werkzeug.socket",
    "werkzeug.request"
]
"""List of keys to be ignored during the serialization process."""


def delete_value(data: dict[Any], key: str) -> None:
    """Delete a specific key-value pair from a dictionary.

    Attempts to remove a key from the dictionary's `environ` key.

    Notes:
        - The function is primarily used during the serilization of Werkzeug's 
            Request object. 

    Args:
        - `data` (dict[Any]): The dictionary from which the key-value pair will 
            be deleted. 
        - `key` (str): The key that needs to be deleted. 

    Raises:
        - `KeyError`: If the value doesn't exist gracefully ignore it. 
    """

    try:
        del data["environ"][key]
    except KeyError as e:
        logger.debug(f"Key {key} not found on object during serilization")
        pass


def delete_ignored(data: dict[Any]) -> None:
    """Delete ignored keys from the dictionary.

    Args:
        - `data` (dict[Any]): The dictionary from which the ignored keys will be 
            deleted.

    Raises:
        - `KeyError`: If the value doesn't exist gracefully ignore it.

    Returns:
        `None`: Void
    """

    try:
        del data["stream"]
    except KeyError as e:
        pass
    for key in IGNORE_KEYS:
        delete_value(data, key)


def serializer(obj: Any) -> Union[str, dict, None]:
    """Custom JSON serializer function.

    This function is intended to serialize various types of objects into 
    JSON-friendly formats. It turns datetime objects into string format and 
    Werkzeug's Request object into a simplified dictionary. It encodes files
    which can be base64 decoded at a later time.

    Args:
        - `obj` (Any): The object that needs to be serialized.

    Raises:
        - `TypeError`: If the object type is not serializable.

    Returns:
        - `Union[str, dict, None]`: The serialized object.
    """

    if isinstance(obj, (datetime, date, time)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Request):
        return process_request(obj)
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, EnvironHeaders):
        return dict(obj)
    elif isinstance(obj, FileStorage):
        file_content = obj.read()
        base64_encoded = base64.b64encode(file_content).decode('utf-8')
        obj.seek(0)  # Important if the obj will be read later
        return {
            'filename': obj.filename,
            'content_type': obj.content_type,
            'data': base64_encoded
        }
    raise TypeError(f"Type {type(obj)} not serializable")


def process_request(obj: Request) -> dict:
    """Process a Werkzeug Request object and return a serialized dictionary 
    representation.

    Takes a Werkzeug Request object and processes it into a dictionary suitable 
    for serialization. It binds various parts of the request to the dictionary, 
    deletes ignored keys, and sorts the keys in the dictionary.

    Args:
        - `obj` (`Request`): The Werkzeug Request object to be processed.

    Returns:
        `dict`: A dictionary representation of the processed request.
    """

    data = vars(obj)
    bind_args(data, obj)
    bind_json(data, obj)
    bind_form(data, obj)
    delete_ignored(data)
    sort_response(data)
    return data


def bind_form(data: dict[Any], obj: Request) -> None:
    """Bind form data to the dictionary.

    Args:
        - `data` (dict[Any]): The dictionary to which the form data will be bound.
        - `obj` (`Request`): The Werkzeug Request object.

    Raises:
        - `KeyError`: If the value doesn't exist gracefully ignore it.

    Returns:
        `None`: Void
    """

    try:
        data["form"] = obj.form.to_dict()
    except UnsupportedMediaType as e:
        data["form"] = {}
    except KeyError as e:
        data["form"] = {}
        pass
    except Exception as e:
        data["form"] = {}
        pass


def bind_args(data: dict[Any], obj: Request) -> None:
    """Bind arguments to the dictionary.

    Args:
        - `data` (dict[Any]): The dictionary to which the arguments will be bound.
        - `obj` (`Request`): The Werkzeug Request object.

    Raises:
        - `KeyError`: If the value doesn't exist gracefully ignore it.

    Returns:
        `None`: Void
    """

    try:
        data["args"] = obj.args
    except UnsupportedMediaType as e:
        data["args"] = {}
    except KeyError as e:
        data["args"] = {}
        pass
    except Exception as e:
        data["args"] = {}
        pass


def bind_json(data: dict[Any], obj: Request) -> None:
    """Bind JSON data to the dictionary.

    Args:
        - `data` (dict[Any]): The dictionary to which the JSON data will be bound.
        - `obj` (`Request`): The Werkzeug Request object.

    Raises:
        - `KeyError`: If the value doesn't exist gracefully ignore it.

    Returns:
        `None`: Void
    """

    try:
        data["json"] = obj.json
    except UnsupportedMediaType as e:
        data["json"] = {}
    except KeyError as e:
        data["json"] = {}
        pass
    except Exception as e:
        data["json"] = {}
        pass


def sort_response(data: dict[Any]) -> None:
    """Sort dictionary keys and relocate the 'files' key.

    Args:
        - `data` (dict[Any]): The dictionary that needs sorting.

    Returns:
        `None`: Void
    """

    data = {
        k: data[k]
        for k in sorted(data)
        if not k.lower().startswith("_")
    }
    files_value = data.pop("files")
    data["files"] = files_value
