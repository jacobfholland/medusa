import os
import sys

path = os.path.abspath("./../..")
sys.path.insert(0, path)


project = "Medusa"
copyright = "2023, Jacob Holland"
author = "Jacob Holland"
release = "0.0.1"
extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_context = {
    "display_github": True,
    "github_user": "jacobfholland",
    "github_repo": "medusa",
    "github_version": "master",
    "conf_py_path": f"/docs/sphinx/"
}
