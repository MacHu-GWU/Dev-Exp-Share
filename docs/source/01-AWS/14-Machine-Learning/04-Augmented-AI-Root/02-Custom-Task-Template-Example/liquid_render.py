# -*- coding: utf-8 -*-

"""
This is a utility script allow you to debug your AWS Augmented AI Task Template
locally.

Copyright (c) 2021-2022, Sanhe Hu.
License: MIT (see LICENSE for details)

Pre-requisite:

- ``Python >= 3.7``, ``python_liquid``, ``python_box``

.. code-block:: bash

    pip install python_liquid
    pip install python_box
"""

import json
from pathlib import Path
from box import Box
from liquid import Template

dir_here = Path(__file__).parent
path_template = Path(dir_here, "task-backup.liquid")
path_data = Path(dir_here, "task.json")
path_html = Path(dir_here, "task.html")

# read liquid template
template = Template(path_template.read_text())

# read task data
input_data = json.loads(path_data.read_text())

# convert task data to box, so it support dot notation
task = Box({"input": input_data})

# render template
content = template.render(task=task)

# write template to html file
path_html.write_text(content)
