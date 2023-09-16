import ast
import glob
import importlib.util
import os
import sys
from typing import Any, Dict, List, Type, Union

from app.config import Config

from .logger import logger


def check_project_directory(project_directory: str) -> bool:
    """
    Check if the specified project directory exists.

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
    """
    Get all Python files in a project directory recursively.

    Args:
        project_directory (str): The path to the project directory.

    Returns:
        List[str]: List of paths to Python files.
    """

    return [f for f in glob.glob(f"{project_directory}/**/*.py", recursive=True) if "__pycache__" not in f and not any(env in f for env in ["venv", "env", ".env"])]


def import_class_from_file(python_file: str, class_name: str) -> Any:
    """
    Import a Python class from a file.

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


def import_routes() -> Dict[str, Any]:
    if not check_project_directory(Config.APP_DIR):
        return sys.exit(1)
    logger.info("Initializing register routes")
    routes = []
    python_files = filter_python_files(Config.APP_DIR)
    for python_file in python_files:
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)
        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                parent_names = [
                    base.id for base in node.bases if isinstance(base, ast.Name)]

                if "Route" in parent_names and not node.name == "Model":
                    class_obj = import_class_from_file(
                        python_file, node.name
                    )()
                    routes.append(class_obj)
                    logger.debug(
                        f"Imported routes for {node.name} from {python_file} for import")
    logger.debug(routes)
    logger.info("Registering routes completed")
    return routes


def import_models() -> Dict[str, Any]:
    if not check_project_directory(Config.APP_DIR):
        return sys.exit(1)
    logger.info("Initializing models import")
    models = []
    python_files = filter_python_files(Config.APP_DIR)
    for python_file in python_files:
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parent_names = [
                    base.id for base in node.bases if isinstance(base, ast.Name)]
                if "Model" in parent_names:
                    class_obj = import_class_from_file(
                        python_file, node.name
                    )
                    models.append(class_obj())
                    logger.debug(
                        f"Imported models for {node.name} from {python_file} for import")
    logger.debug(models)
    logger.info("Importing models completed")
    return models
