from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import os

def create_pdf_from_svgs(svg_files, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    for svg in svg_files:
        drawing = svg2rlg(svg)
        if drawing:
            drawing.scale(1, 1)
            renderPDF.draw(drawing, c, 0, 0)
            if svg != svg_files[-1]:
                c.showPage()
    c.save()

svg_files = [
    "aboba.svg",
    "aboba2.svg",
]

create_pdf_from_svgs(svg_files, "output.pdf")
