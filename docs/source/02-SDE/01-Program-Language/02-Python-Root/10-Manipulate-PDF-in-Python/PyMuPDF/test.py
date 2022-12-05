# -*- coding: utf-8 -*-

"""
Reference:

- https://pypi.org/project/PyMuPDF/
"""

from io import BytesIO
import fitz  # This is the PyMuPDF import name
from pathlib import Path

dir_here = Path(__file__).absolute().parent

# --- Set the sample PDF file path you want to test with
path_w2_pdf = dir_here.parent / "w2.pdf"

path_pdf = path_w2_pdf

# You can use either ``fitz.Document(filename=...)``
# or use bytes stream ``fitz.Document(stream=...)`` to read the PDF content
doc = fitz.Document(stream=path_pdf.read_bytes())

# Repair any issues (hopefully) before we hit them
# See this https://github.com/pymupdf/PyMuPDF/issues/856
buffer = BytesIO()
buffer.write(doc.write(clean=True, garbage=4))  # write the document to in-memory buffer
new_content = buffer.getvalue()
buffer.close()
doc = fitz.Document(stream=new_content)

for page_num, page in enumerate(doc, start=1):
    # --- split page
    doc1 = fitz.Document()  # new empty PDF
    # doc1.insert_pdf(doc, from_page=page_num-1, to_page=page_num-1)
    doc1.insert_pdf(doc)
    p = dir_here / f"{path_pdf.stem}-page-{page_num}.pdf"
    # you cannot write document to io.BytesIO
    doc1.save(f"{p}")

    # --- convert page to image
    pix: fitz.Pixmap = page.get_pixmap(dpi=200)
    p = dir_here / f"{path_pdf.stem}-{page_num}.png"
    # you cannot write pix map to io.BytesIO
    pix.save(f"{p}", output="png")
