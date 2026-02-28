from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

import os

def create_pdf_from_files(files, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    for img in files:
        if '.svg' in img:
            drawing = svg2rlg(img)
        elif '.png' in img:
            drawing = Image(img)
        if drawing:
            drawing.scale(1, 1)
            renderPDF.draw(drawing, c, 0, 0)
            if img != files[-1]:
                c.showPage()
    c.save()