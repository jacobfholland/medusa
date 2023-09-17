import ast
import sys
from typing import Any, Dict
from app.config import Config
from app.server.logger import logger
from utils.importing import check_project_directory, filter_python_files, import_class_from_file


def import_routes() -> Dict[str, Any]:
    if not check_project_directory(Config.APP_DIR):
        return sys.exit(1)
    logger.info("Initializing routes import")
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
                    )
                    class_obj.routes()
                    routes.append(class_obj.__name__)
                    logger.debug(
                        f"Registered routes for {node.name} from {python_file} for import")
    logger.debug(routes)
    logger.info("Importing routes completed")
    return routes
