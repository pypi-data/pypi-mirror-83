#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
personroles documentation build configuration file

This file has the current directory set to its containing dir.

All configuration values have a default; values that are commented out serve to
show the default.

If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.
"""

import importlib
import os
import os.path
import sys
from typing import Dict  # noqa

# from six import string_types
# from sphinx import version_info

PACKAGE_PARENT = ".."
DOCS_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
PROJECT_DIR = os.path.dirname(DOCS_DIR)
sys.path.insert(0, PROJECT_DIR)
sys.path.append(
    os.path.normpath(os.path.join(DOCS_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

# from src import person  # noqa
#
# print(person.__path__)

# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "personroles"
copyright = "2020, Oliver Stapel"
author = "Oliver Stapel"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
# version = person.__version__
verson = "0.1.8"
# The full version, including alpha/beta/rc tags.
# release = person.__version__
release = "0.1.8"


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**tests**",
    "**setup**",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Extensions
# ==========

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # Import docstrings from modules, classes, functions and more.
    # http://sphinx-doc.org/ext/autodoc.html
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    # Google/Numpy-style docstring support
    # http://sphinx-doc.org/ext/napoleon.html#module-sphinx.ext.napoleon
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

# autodoc
# -------

# http://sphinx-doc.org/ext/autodoc.html#confval-autodoc_default_flags
autodoc_default_flags = (
    "members",
    "undoc-members",
)

# http://sphinx-doc.org/ext/autodoc.html#confval-autodoc_member_order
autodoc_member_order = "alphabetical"

# http://sphinx-doc.org/ext/autodoc.html#confval-autoclass_content
# Include docstrings from: class || init || both
autoclass_content = "class"


# doctest
# -------
#
# doctest_global_setup = "from api_browser import *"
#
#
# InterSphinx
# -----------
#
# intersphinx_mapping = {
#    "python": ("http://python.readthedocs.org/en/v2.7.2/", None),
#    "sphinx": ("http://sphinx.readthedocs.org/en/latest/", None),
# }

# Output
# ======

# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "persondoc"

# -- Options for LaTeX output ------------------------------------------

latex_elements: Dict[str, str] = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "person.tex",
        "personroles Documentation",
        "Oliver Stapel",
        "manual",
    ),  # noqa
]  # noqa


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "personroles", "personroles Documentation", [author], 1)
]  # noqa


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "personroles",
        "personroles Documentation",
        author,
        "personroles",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# Add RTD Static Path. Add to the end because it overwrites previous files.
if 'html_static_path' not in globals():
    html_static_path = []
if os.path.exists('_static'):
    html_static_path.append('_static')

# Add RTD Theme only if they aren't overriding it already
using_rtd_theme = (
    (
        'html_theme' in globals() and
        html_theme in ['default'] and
        # Allow people to bail with a hack of having an html_style
        'html_style' not in globals()
    ) or 'html_theme' not in globals()
)
if using_rtd_theme:
    theme = importlib.import_module('sphinx_rtd_theme')
    html_theme = 'sphinx_rtd_theme'
    html_style = None
    html_theme_options: Dict = {}
#     if 'html_theme_path' in globals():
#         html_theme_path.append(theme.get_html_theme_path())
#     else:
#         html_theme_path = [theme.get_html_theme_path()]

if globals().get('websupport2_base_url', False):
    websupport2_base_url = 'https://readthedocs.org/websupport'
    websupport2_static_url = 'https://assets.readthedocs.org/static/'


# Add project information to the template context.
context = {
    'using_theme': using_rtd_theme,
    'html_theme': html_theme,
    'current_version': "latest",
    'version_slug': "latest",
    'MEDIA_URL': "https://media.readthedocs.org/",
    'STATIC_URL': "https://assets.readthedocs.org/static/",
    'PRODUCTION_DOMAIN': "readthedocs.org",
    'versions': [("latest", "/en/latest/"), ],
    'downloads': [
        # ("pdf", "//person.readthedocs.io/_/downloads/en/latest/pdf/"),
        ("html", "//person.readthedocs.io/_/downloads/en/latest/htmlzip/"),
        # ("epub", "//person.readthedocs.io/_/downloads/en/latest/epub/"),  # noqa
    ],
    'subprojects': [
    ],
    'slug': 'personroles',
    'name': u'personroles',
    'rtd_language': u'en',
    'programming_language': u'words',
    'canonical_url': 'https://person.readthedocs.io/en/latest/',
    'analytics_code': 'None',
    'single_version': False,
    'conf_py_path': '/docs/',
    'api_host': 'https://readthedocs.org',
    'github_user': '0LL13',
    'proxied_api_host': '/_',
    'github_repo': 'person',
    'github_version': 'master',
    'display_github': True,
    'READTHEDOCS': True,
    'new_theme': (html_theme == "sphinx_rtd_theme"),
    'ad_free': False,
    'docsearch_disabled': False,
}

# if 'html_context' in globals():
#     html_context.update(context)
# else:
#     html_context = context

# Add custom RTD extension
# if 'extensions' in globals():
#     # Insert at the beginning because it can interfere
#     # with other extensions.
#     # See https://github.com/rtfd/readthedocs.org/pull/4054
#     extensions.insert(0, "readthedocs_ext.readthedocs")
# else:
#     extensions = ["readthedocs_ext.readthedocs"]

# Add External version warning banner to the external version documentation
if 'branch' == 'external':
    extensions.insert(1, "readthedocs_ext.external_version_warning")

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# User's Sphinx configurations
language_user = globals().get('language', None)
latex_engine_user = globals().get('latex_engine', None)
latex_elements_user = globals().get('latex_elements', None)

# Remove this once xindy gets installed in Docker image and XINDYOPS
# env variable is supported
# https://github.com/rtfd/readthedocs-docker-images/pull/98
latex_use_xindy = False

# Make sure our build directory is always excluded
exclude_patterns = globals().get('exclude_patterns', [])
exclude_patterns.extend(['_build'])
