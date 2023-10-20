import functools
from logging import Logger
import sys
from typing import Callable, List

from .logger import logger


def require_envs(config: object, envs: List[str]) -> Callable:
    """A decorator that checks if the specified environment variables are present.

    Args:
        - ``config`` (object): The configuration object that should contain the 
          environment variables.
        - ``envs`` (List[str]): A list of environment variable names to check for.

    Func Args:
        - ``**args`` (dict): Source function positional arguments.
        - ``**kwargs`` (dict): Source function key word arguments.

    Returns:
        ``Callable``: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_envs(config, envs):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def check_envs(config: object, envs: List[str]) -> bool:
    """Checks if the specified environment variables are present. If specified 
    environment variables are not present, it will exit running the application.

    Args:
        - ``config`` (object): The configuration object that should contain the 
          environment variables.
        - ``envs`` (List[str]): A list of environment variable names to check for.

    Func Args:
        - ``**args`` (dict): Source function positional arguments.
        - ``**kwargs`` (dict): Source function key word arguments.

    Returns:
        ``bool``: If the environment variable is present.
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


def log_env_vars(Config: object, logger: Logger) -> None:
    """Logs the environment variables from the provided configuration. If the 
    `APP_MASK` attribute is set to True in the Config, the variable values will be 
    redacted in the logs.

    Args:
        - ``Config`` (object): The configuration object containing the environment 
          variables to be logged.
        - ``logger`` (Logger): The logger instance to which the environment variables 
          will be logged.

    Returns:
        ``None``: Void.
    """

    for k, v in Config.__dict__.items():
        if not k.startswith("_"):
            if Config.APP_MASK:
                v = "[REDACTED]"
            logger.debug(f"{k}: {v}")
