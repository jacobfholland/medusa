import os
import ast
import glob
import importlib.util
import sys
from typing import Dict, List, Type, Union, Any
from config.app import Config
from app.database.logger import logger
from app.database.model import Model


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

    spec = importlib.util.spec_from_file_location("temp_module", python_file)
    temp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_module)
    return getattr(temp_module, class_name)


def import_models(database_instance: Union[Type, Any]) -> Dict[str, Any]:
    """
    Import all models that inherit from 'Model' from all Python files
    in a specified project directory.

    Args:
        database_instance (Union[Type, Any]): An instance of the database.

    Returns:
        Dict[str, Any]: A dictionary mapping class names to class objects.
    """

    if not check_project_directory(Config.APP_DIR):
        return sys.exit(1)
    logger.info("Initializing model import")
    models = {}
    python_files = filter_python_files(Config.APP_DIR)
    for python_file in python_files:
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parent_names = [
                    base.id for base in node.bases if isinstance(base, ast.Name)]
                if 'Model' in parent_names:
                    class_obj = import_class_from_file(python_file, node.name)
                    if class_obj is not Model:
                        models[node.name] = class_obj
                        database_instance.all_models.append(class_obj)
                        logger.debug(
                            f"Staging class {node.name} from {python_file} for import")
    logger.debug(models)
    logger.info("Model import completed")
    return models
