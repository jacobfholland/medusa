import ast
import sys
from typing import Any, Dict
from app.config import Config

from app.database.logger import logger
from utils.importing import check_project_directory, filter_python_files, import_class_from_file


def import_models() -> Dict[str, Any]:
    init_db()
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
                # Import the class into the current namespace.
                class_obj = import_class_from_file(python_file, node.name)

                # Check if "Model" is in the list of ancestors.
                if 'Model' in [base.__name__ for base in class_obj.mro()]:
                    class_obj.register_model()
                    models.append(class_obj.__name__)
                    logger.debug(
                        f"Imported model {node.name} from {python_file} for import"
                    )

    logger.debug(models)
    logger.info("Importing models completed")

    return models


def init_db():
    from app.database.base import Base
