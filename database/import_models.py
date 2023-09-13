import ast
import glob
import os
from database.model import Model
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


def import_models(database_instance):
    project_directory = "/home/jacob/devtools/medusa2"
    if not os.path.exists(project_directory):
        print(
            f"The specified project directory '{project_directory}' does not exist.")
        return

    models = {}
    python_files = glob.glob(
        f"{project_directory}/**/*.py", recursive=True)

    for python_file in python_files:
        if "__pycache__" in python_file or any(env_folder in python_file for env_folder in ["venv", "env", ".env"]):
            continue

        with open(python_file, 'r') as f:
            tree = ast.parse(f.read(), filename=python_file)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parent_names = [
                    base.id for base in node.bases if isinstance(base, ast.Name)]

                if 'Model' in parent_names:
                    spec = importlib.util.spec_from_file_location(
                        "temp_module", python_file)
                    temp_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(temp_module)
                    class_obj = getattr(temp_module, node.name)

                    # Don't import the 'Model' class itself
                    if class_obj is not Model:
                        models[node.name] = class_obj
                        database_instance.all_models.append(class_obj)
                        print(
                            f"Staging class {node.name} from {python_file} for import")
    return models
