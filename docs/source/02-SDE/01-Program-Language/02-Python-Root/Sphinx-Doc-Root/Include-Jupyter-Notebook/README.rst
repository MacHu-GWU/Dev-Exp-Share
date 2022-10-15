Sphinx Doc - Include Jupyter Notebook
==============================================================================
Keywords: Sphinx Doc, Jupyter Notebook, Jupyter Lab, JupyterNotebook, JupyterLab


Summary
------------------------------------------------------------------------------
介绍如何在 Sphinx Doc 文档中嵌入 Jupyter Notebook.

1. Install `nbsphinx <https://pypi.org/project/nbsphinx/>`_.
2. Add extension to your sphinx doc ``conf.py`` file.

.. code-block:: python

    extensions = [
        "nbsphinx",
    ]

3. Include notebook in RestructuredText.

.. code-block:: ReST

    .. toctree::
       :maxdepth: 2
       :caption: Contents:

       notebooks/Example 1

4. Make sure you add ``IPython`` to your ``requirements-doc.txt`` file, otherwise the Sphinx Doc cannot show **Syntax Highlight** in Code Block.

Reference:

- https://docs.readthedocs.io/en/stable/guides/jupyter.html
- https://nbsphinx.readthedocs.io/en/0.8.9/