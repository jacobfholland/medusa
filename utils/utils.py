import ast
import glob
import os
import uuid
from logger.logger import logger
import sys
import ast
import importlib
import os
import sys
from pathlib import Path
import os
import glob
import importlib.util


def require_envs(config, envs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            false_envs = [
                env for env in envs
                if not vars(config).get(env)
            ]
            if false_envs:
                logger.error(
                    f"Missing required environment variables: {', '.join(false_envs)}"
                )
                return sys.exit(1)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def generate_uuid():
    """
    Generate a unique identifier using uuid.

    Returns:
        str: Generated unique identifier.
    """

    return str(uuid.uuid4())
