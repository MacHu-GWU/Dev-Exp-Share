Include Jupyter Notebook in Sphinx Doc
==============================================================================
Keywords:

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

Reference:

- https://docs.readthedocs.io/en/stable/guides/jupyter.html
- https://nbsphinx.readthedocs.io/en/0.8.9/