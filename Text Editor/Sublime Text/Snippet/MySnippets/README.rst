Edit Your Own Code Snippet and Activate them in Sublime Text, Atom and PyCharm
==============================================================================
You could write your own snippet in this format, fill in ``{{ scope }}``, ``{{ description }}``, ``{{ trigger }}``, ``{{ content }}``, following `This Guide <http://docs.sublimetext.info/en/latest/extensibility/snippets.html>`_), and save with ``{{ unique-snippet-name.sublime-snippet }}``:

.. code-block:: html

    <snippet>
        <scope>{{ scope }}</scope>
        <description>{{ description }}</description>
        <tabTrigger>{{ trigger }}</tabTrigger>
        <content><![CDATA[
    {{ content }}
    ]]></content>
    </snippet>

Make sure your snippet files are under ``MySnippets`` Folder.

Then just run ``transform.py`` in Python (Python27, 34, 35, 36) file. Your snippet will be available to use in Sublime Text, Atom and PyCharm.

Dependencies:

- lxml
- beautifulsoup4
- pathlib_mate