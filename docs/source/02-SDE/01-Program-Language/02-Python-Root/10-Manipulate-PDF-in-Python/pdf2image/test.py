# -*- coding: utf-8 -*-

"""
- Pypi: https://pypi.org/project/pdf2image/

Dependencies:

Mac:

- Install `poppler for Mac <https://macappstore.org/poppler/>`_
- do ``brew install poppler``
- use ``brew list poppler`` to figure out the poppler bin folder, on my computer it is ``/opt/homebrew/Cellar/poppler/22.08.0/bin/``

Linux (Redhat):

- Install poppler for Linux ``sudo yum install poppler-utils``
- Check it is installed ``yum list poppler-utils``
"""

from pathlib import Path
from pdf2image import convert_from_path

dir_here = Path(__file__).absolute().parent
path_w2_pdf = dir_here.parent / "w2.pdf"

images = convert_from_path(
    f"{path_w2_pdf}",
    dpi=300,
    fmt="png",
    # poppler_path="/opt/homebrew/Cellar/poppler/22.08.0/bin/", # don't need this on Linux
)
for page_num, image in enumerate(images, start=1):
    path_output = dir_here / f"page-{page_num}.png"
    image.save(f"{path_output}")
