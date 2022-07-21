# Python itself use RST to write it's document
# doctuils is the built in library to process RST file

import docutils.core

docutils.core.publish_file(
    source_path="README.rst",
    destination_path="README.html",
    writer_name="html"
)
