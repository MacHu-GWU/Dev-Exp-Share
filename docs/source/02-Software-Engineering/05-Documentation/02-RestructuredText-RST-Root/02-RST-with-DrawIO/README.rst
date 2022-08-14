RestructuredText RST with DrawIO
==============================================================================


Summary
------------------------------------------------------------------------------
RestructuredText is awesome, and draw.io is also awesome, how could I embed a draw.io diagram in RST document?

1. Create your Diagram in DrawIO, save as XML with ``.drawio`` file extension. This is where you edit your diagram.
2. Once you are happy with the diagram, export it as HTML.
3. In you RST document, embed the draw.io HTML with the ``raw`` derivative. Now you can view it in many viewer, like Sublime RST Render, VSCode Render, PyCharm Render, preview on GitHub, or build Sphinx Doc.

.. code-block:: ReST

    .. raw:: html
        :file: ./diagram.drawio.html

4. If you want to share it to other people, use this python code to export the entire RST document as a HTML file, it will embed the draw.io HTML inline as it is instead of referencing external file. So you can easily share it to other people with only ONE HTML file.

.. code-block:: python

    # Python itself use RST to write it's document
    # doctuils is the built in library to process RST file

    import docutils.core

    docutils.core.publish_file(
        source_path="README.rst",
        destination_path="README.html",
        writer_name="html"
    )

5. If you want to export it as a PDF, you have to ensure you only have one TAB in each draw.io diagram. If you have 3 tab in one draw.io diagram, you should re-create 3 draw.io HTML files. You can export it to HTML first, open in Chrome browser, then click on ``Print`` -> ``Export as PDF``.


Example
------------------------------------------------------------------------------
**This is the Multi Tab Diagram**

You can see both tab in HTML, but only see one tab in PDF

.. raw:: html
    :file: ./diagram.drawio.html

**This is the correct way to handle Multi Tab Diagram**

.. raw:: html
    :file: ./diagram1.drawio.html

.. raw:: html
    :file: ./diagram2.drawio.html
