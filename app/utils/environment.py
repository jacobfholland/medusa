import functools
import sys
from typing import Callable, List

from .logger import logger


def require_envs(config: object, envs: List[str]) -> Callable:
    """
    A decorator that checks if the specified environment variables are present.

    Args:
        config (object): The configuration object that should contain the environment variables.
        envs (List[str]): A list of environment variable names to check for.

    Returns:
        Callable: The decorated function.
    """

    def check_envs(config: object, envs: List[str]) -> bool:
        """
        Check if the specified environment variables are present in the configuration object.

        Args:
            config (object): The configuration object.
            envs (List[str]): A list of environment variable names to check.

        Returns:
            bool: True if all environment variables are present; False otherwise.

        Raises:
            SystemExit: If any of the required environment variables are missing, the function will exit with status code 1.
        """

        false_envs = [
            env for env in envs
            if not vars(config).get(env)
        ]
        if false_envs:
            logger.error(
                f"Missing required environment variables: {', '.join(false_envs)}"
            )
            sys.exit(1)
        return True

    def decorator(func: Callable) -> Callable:
        """
        Decorator function to check environment variables before executing the decorated function.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_envs(config, envs):
                return func(*args, **kwargs)
        return wrapper

    return decorator
