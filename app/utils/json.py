from datetime import date, datetime, time
import functools
import json
from flask import jsonify


def serialize(obj):
    """
    Serializes an object to JSON format.
    Args:
        obj (object): The object to serialize.
    Returns:
        str or dict: The serialized object.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, time):
        return obj.isoformat()
    return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}


def json_serializer(obj):
    """
    Converts an object to a JSON string.
    Args:
        obj (object): The object to convert.
    Returns:
        str: The JSON string representation of the object.
    """
    if obj is None:
        return 'null'
    return json.dumps(obj, default=serialize)


def to_json(func):
    """
    To JSON
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return json.dumps(None)  # Return 'null' string for None
        return json_serializer(result)
    return wrapper
