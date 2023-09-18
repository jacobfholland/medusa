import os
import sys
path = os.path.abspath("./..")
sys.path.insert(0, path)


project = 'Medusa'
copyright = '2023, Jacob Holland'
author = 'Jacob Holland'
release = '0.0.1'
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster'
html_static_path = ['_static']
