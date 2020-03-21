# -*- coding: utf-8 -*-
#
# dev_exp_share documentation build configuration file, created by
# sphinx-quickstart on Mon Jul 1 00:00:00 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from __future__ import unicode_literals
import os
from datetime import datetime
import dev_exp_share

from docfly.doctree import ArticleFolder
ArticleFolder._filename = "README.rst"

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinxcontrib.jinja',
    'sphinx_copybutton',
    'docfly.directives',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'README'

# General information about the project.
project = 'dev_exp_share'
copyright = '%s, Sanhe Hu' % datetime.utcnow().year
author = 'Sanhe Hu'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = dev_exp_share.__version__
# The full version, including alpha/beta/rc tags.
release = dev_exp_share.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = "./_static/dev_exp_share-logo.png"
html_favicon = "./_static/dev_exp_share-favicon.ico"

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'dev_exp_sharedoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
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
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'dev_exp_share.tex', 'dev_exp_share Documentation',
     u'Sanhe Hu', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'dev_exp_share', 'dev_exp_share Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'dev_exp_share', 'dev_exp_share Documentation',
     author, 'dev_exp_share', 'One line description of project.',
     'Miscellaneous'),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

autodoc_member_order = 'bysource'

# Enable custom css
try:
    custom_style_file_path = os.path.join(os.path.dirname(__file__), "_static", ".custom-style.rst")
    with open(custom_style_file_path, "rb") as f:
        custom_style_file_content = f.read().decode("utf-8")
    rst_prolog = "\n" + custom_style_file_content + "\n"
except:
    pass

# Add data for Jinja2
try:
    from dev_exp_share.docs import doc_data
except:
    doc_data = dict()

jinja_contexts = {
    "doc_data": {
        "doc_data": doc_data,
    },
}

# Api Reference Doc
import docfly

package_name = dev_exp_share.__name__
docfly.ApiReferenceDoc(
    conf_file=__file__,
    package_name=package_name,
    ignored_package=[
        "%s.pkg" % package_name,
        "%s.docs" % package_name,
        "%s.tests" % package_name,
    ]
).fly()


def setup(app):
    app.add_stylesheet('css/custom-style.css')
    app.add_javascript('js/sorttable.js')
