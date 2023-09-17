import ast
import glob
import importlib.util
import os
import sys
from typing import Any, List

from .config import UtilsConfig as Config
from .logger import logger


def check_project_directory(project_directory: str) -> bool:
    """Check if the specified project directory exists.

    Args:
        project_directory (str): The path to the project directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """

    if not os.path.exists(project_directory):
        logger.error(
            f"The specified project directory '{project_directory}' does not exist.")
        return False
    return True


def filter_python_files(project_directory: str) -> List[str]:
    """Get all Python files in a project directory recursively.

    Args:
        project_directory (str): The path to the project directory.

    Returns:
        List[str]: List of paths to Python files.
    """

    return [
        f for f in glob.glob(f"{project_directory}/**/*.py", recursive=True)
        if "__pycache__" not in f
        and not any(env in f for env in ["venv", "env", ".env"])
    ]


def import_class_from_file(python_file: str, class_name: str) -> Any:
    """Import a Python class from a file.

    Args:
        python_file (str): The path to the Python file.
        class_name (str): The name of the class to import.

    Returns:
        Any: The imported class object.
    """

    spec = importlib.util.spec_from_file_location("module", python_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def import_classes(func: callable, import_type: str) -> List[str]:
    """Import classes from Python files in the project directory.

    Args:
        func (callable): The import function (import_model or import_route).
        import_type (str): The type of import ("model" or "route").

    Returns:
        List[str]: List of imported class names.
    """

    if not check_project_directory(Config.APP_DIR):
        return sys.exit(1)
    classes = []
    python_files = filter_python_files(Config.APP_DIR)
    log_starting(import_type)
    for python_file in python_files:
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)
        for node in ast.walk(tree):
            func(node, python_file, classes)
    log_completed(import_type, classes)
    return classes


def log_starting(import_type: str) -> None:
    """Log the start of the import process.

    Args:
        import_type (str): The type of import ("model" or "route").
    """

    if import_type == "model":
        logger.info("Initializing models import")
    elif import_type == "route":
        logger.info("Registering routes")


def log_completed(import_type: str, classes: List[str]) -> None:
    """Log the completion of the import process.

    Args:
        import_type (str): The type of import ("model" or "route").
        classes (List[str]): List of imported class names.
    """

    if import_type == "model":
        logger.debug(f"Models({classes})")
        logger.info("Models import completed")
    elif import_type == "route":
        logger.debug(f"Routes({classes})")
        logger.info("Route registration completed")


def import_model(node: ast.AST, python_file: str, models: List[str]) -> None:
    """Import models from Python files.

    Args:
        node (ast.AST): The AST node.
        python_file (str): The path to the Python file.
        models (List[str]): List of imported model class names.
    """

    if isinstance(node, ast.ClassDef):
        class_obj = import_class_from_file(python_file, node.name)
        cls_name = class_obj.__name__
        if 'Model' in [base.__name__ for base in class_obj.mro()]:
            if not cls_name == "Model":
                try:
                    from app.database.database import Database
                    class_obj.register_model()
                    models.append(cls_name)
                    logger.debug(
                        f"Imported model {node.name} from {python_file}")
                except ImportError as e:
                    logger.warning(
                        f"Did not import model {cls_name} - Database package missing")


def import_route(node: ast.AST, python_file: str, routes: List[str]) -> None:
    """Register routes from Python files.

    Args:
        node (ast.AST): The AST node.
        python_file (str): The path to the Python file.
        routes (List[str]): List of registered route class names.
    """

    if isinstance(node, ast.ClassDef):
        parent_names = [
            base.id for base in node.bases if isinstance(base, ast.Name)]
        if "Route" in parent_names and not node.name == "Model":
            class_obj = import_class_from_file(python_file, node.name)
            cls_name = class_obj.__name__
            try:
                from app.server.server import Server
                class_obj.routes()
                routes.append(cls_name)
                logger.debug(
                    f"Registered routes for {node.name} from {python_file}")
            except ImportError:
                logger.warning(
                    f"Did not register {cls_name} routes - Server package missing")
