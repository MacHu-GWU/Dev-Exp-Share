# -*- coding: utf-8 -*-

import io
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

dir_here = Path(__file__).absolute().parent
path_w2_pdf = dir_here.parent / "w2.pdf"

reader = PdfReader(io.BytesIO(path_w2_pdf.read_bytes()))
n_page = len(reader.pages)
for i in range(n_page):
    writer = PdfWriter()
    writer.add_page(reader.pages[i])
    page = i + 1
    buffer = io.BytesIO()
    writer.write(buffer)
    path_dst = dir_here / f"{page}.pdf"
    path_dst.write_bytes(buffer.getvalue())
