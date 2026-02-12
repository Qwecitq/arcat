### first install Sphinx Auto Documentation Using "pip install sphinx sphinx-rtd-theme"
import os
import sys
sys.path.insert(0, os.path.abspath("../"))

project = "arcat"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
html_theme = "sphinx_rtd_theme"
