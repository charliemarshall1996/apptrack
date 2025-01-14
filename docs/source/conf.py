# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import django
import sys
import os
project = 'AppTrack'
copyright = '2025, Charlie Marshall'
author = 'Charlie Marshall'
release = 'v1.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

sys.path.insert(0, os.path.abspath('../../apptrack'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'apptrack.settings'
django.setup()
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
