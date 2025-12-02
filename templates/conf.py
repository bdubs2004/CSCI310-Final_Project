#UNL_Parking Sphinx configuration file

project = '{{ project }}'
copyright = '{{ copyright }}'
author = '{{ author }}'
release = '{{ release }}'

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

#General Configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
]

templates_path = ['{{ dot }}templates']
exclude_patterns = [{{ exclude_patterns }}]

# Options for HTML output

html_theme = 'alabaster'
html_static_path = ['{{ dot }}static']
