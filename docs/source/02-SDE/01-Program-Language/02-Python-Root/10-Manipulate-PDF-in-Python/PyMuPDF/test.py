# -*- coding: utf-8 -*-

from pathlib import Path
import fitz

dir_here = Path(__file__).absolute().parent
path_w2_pdf = dir_here.parent / "w2.pdf"

# bytes protocol
doc = fitz.open(stream=path_w2_pdf.read_bytes())

for page_num, page in enumerate(doc, start=1):
    # split page
    doc1 = fitz.open()  # new empty PDF
    doc1.insert_pdf(doc, from_page=page_num-1, to_page=page_num-1)
    p = dir_here / f"page-{page_num}.pdf"
    # you cannot write document to io.BytesIO
    doc1.save(f"{p}")

    # convert page to image
    pix = page.get_pixmap(dpi=300)
    p = dir_here / f"page-{page_num}.png"
    # you cannot write pix map to io.BytesIO
    pix.save(f"{p}")