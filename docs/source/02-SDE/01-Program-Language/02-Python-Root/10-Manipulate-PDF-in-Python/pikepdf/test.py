# -*- coding: utf-8 -*-

from pathlib import Path
from pikepdf import Pdf, PdfImage

dir_here = Path(__file__).absolute().parent
path_w2_pdf = dir_here.parent / "w2.pdf"

pdf = Pdf.open(f"{path_w2_pdf}")

for page_num, page in enumerate(pdf.pages, start=1):
    # split page
    dst = Pdf.new()
    dst.pages.append(page)
    path_dst = dir_here / f"page-{page_num}.pdf"
    dst.save(f"{path_dst}")
