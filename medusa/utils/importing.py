import ast
import glob
import importlib.util
import os
import sys
from typing import Any, Callable, List
from medusa.database.base import Engine

from medusa.database.model import Model

from .config import UtilsConfig as Config
from .logger import logger


def check_dir(path: str) -> bool:
    """Check if the specified project directory exists.

    Args:
        - ``path`` (str): The path to the directory to check.

    Returns:
        ``bool``: True if the directory exists, False otherwise.
    """

    if not os.path.exists(path):
        logger.error(
            f"The specified directory '{path}' does not exist.")
        return False
    return True


def python_files(path: str) -> List[str]:
    """Get all Python files in a project directory recursively.

    Args:
        - ``path`` (str): The path to the project directory.

    Returns:
        ``List[str]``: List of paths to Python files.
    """
    # Use os.path.join to construct file path
    pattern = os.path.join(path, "**", "*.py")

    return [
        f for f in glob.glob(pattern, recursive=True)
        if "__pycache__" not in f
        and not any(ignore in f for ignore in ["venv", "env", ".env", "docs"])
    ]


def import_class_from_file(python_file: str, class_name: str) -> Any:
    """Import a Python class from a file.

    Args:
        - ``python_file`` (str): The path to the Python file.
        - ``class_name`` (str): The name of the class to import.

    Returns:
        ``Any``: The imported class object.
    """

    spec = importlib.util.spec_from_file_location("module", python_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def import_classes(func: Callable, import_type: str) -> List[str]:
    """Import classes from Python files in the project directory.

    Args:
        - ``func`` (``Callable``): The import function (`import_model` or `import_route`).
        - ``import_type`` (str): The type of import (`"model"` or `"route"`).

    Returns:
        ``List[str]``: List of imported class names.
    """

    app_dir = Config.APP_DIR
    if not check_dir(app_dir):
        return sys.exit(1)
    classes = []
    files = python_files(app_dir)
    log_starting(import_type)
    for python_file in files:
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)
        for node in ast.walk(tree):
            func(node, python_file, classes)
    log_completed(import_type, classes)
    return classes


def log_starting(import_type: str) -> None:
    """Log the start of the import process.

    Args:
        - ``import_type`` (str): The type of import ("model" or "route").

    Returns:
        ``None``: Void.
    """

    if import_type == "model":
        logger.info("Initializing models import")
    elif import_type == "route":
        logger.info("Registering routes")


def log_completed(import_type: str, classes: List[str]) -> None:
    """Log the completion of the import process.

    Args:
        - ``import_type`` (str): The type of import ("model" or "route").
        - ``classes`` (List[str]): List of imported class names.

    Returns:
        ``None``: Void.
    """

    if import_type == "model":
        logger.debug(f"Models({classes})")
        logger.info("Models import completed")
    elif import_type == "route":
        logger.debug(f"Routes({classes})")
        logger.info("Route registration completed")


def import_model(node: ast.AST, python_file: str, models: List[str]) -> None:
    """Import models from Python files and register them if they inherit from the 
    'Model' base class.

    Args:
        - ``node`` (``AST``): The AST node representing a class definition.
        - ``python_file`` (str): The path to the Python file.
        - ``models`` (List[str]): List of imported model class names.

    Raises:
        - ``ImportError``: If the 'Database' package is missing, models won't be 
          registered.

    Returns:
        ``None``: Void.
    """

    if isinstance(node, ast.ClassDef):
        class_obj = import_class_from_file(python_file, node.name)
        cls_name = class_obj.__name__
        if Model in class_obj.__mro__:
            class_obj.metadata.create_all(Engine)
            models.append(cls_name)
            class_obj.routes(class_obj)
            logger.debug(f"Imported model {node.name} from {python_file}")
        # if 'Model' in [base.__name__ for base in class_obj.mro()]:
        #     if not cls_name == "Model":
        #         try:
        #
        #         except ImportError as e:
        #             logger.warning(
        #                 f"Did not import model {cls_name} - Database package missing")


def import_route(node: ast.AST, python_file: str, routes: List[str]) -> None:
    """Register routes from Python files if they inherit from the 'Route' base class.

    Args:
        - ``node`` (``AST``): The AST node representing a class definition.
        - ``python_file`` (str): The path to the Python file.
        - ``routes`` (List[str]): List of registered route class names.

    Raises:
        - ``ImportError``: If the 'Server' package is missing, routes won't be 
          registered.

    Returns:
        ``None``: Void.
    """

    if isinstance(node, ast.ClassDef):
        parent_names = [
            base.id
            for base in node.bases
            if isinstance(base, ast.Name)
        ]
        if "Route" in parent_names and not node.name == "Route":
            class_obj = import_class_from_file(python_file, node.name)
            cls_name = class_obj.__name__
            try:
                class_obj.routes(class_obj)
                routes.append(cls_name)
                logger.debug(
                    f"Registered routes for {node.name} from {python_file}")
            except ImportError:
                logger.warning(
                    f"Did not register {cls_name} routes - Server package missing")
