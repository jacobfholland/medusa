import functools
import sys
import uuid
from typing import Callable, List

from .logger import logger


def require_envs(config: object, envs: List[str]) -> Callable:
    """
    A decorator that checks if the specified environment variables are present in the config object.

    Args:
        config (object): The configuration object that should contain the environment variables.
        envs (List[str]): A list of environment variable names to check for.

    Returns:
        Callable: The decorated function.
    """

    def check_envs(config, envs):
        false_envs = [
            env for env in envs
            if not vars(config).get(env)
        ]
        if false_envs:
            logger.error(
                f"Missing required environment variables: {', '.join(false_envs)}"
            )
            return sys.exit(1)
        return True

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_envs(config, envs):
                return func(*args, **kwargs)
        return wrapper

    return decorator


def generate_uuid() -> str:
    """
    Generate a unique identifier using uuid.

    Returns:
        str: Generated unique identifier.
    """

    return str(uuid.uuid4())
