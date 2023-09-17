import glob
import importlib
import os
from typing import Any, List
from utils.logger import logger


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
