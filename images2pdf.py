from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import os

def create_pdf_from_files(files, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4
    for img in files:
        if '.svg' in img:
            drawing = svg2rlg(img)
            drawing.wrap(1, 1)
            if drawing:
                aspect = min( page_width / drawing.width
                            , page_height / drawing.height
                            )
                drawing.scale(aspect, aspect)
                renderPDF.draw(drawing, c, 0, 0)
        elif '.png' in img:
            drawing = c.drawImage(img, 0, 0, page_width, page_height)
        if drawing and img != files[-1]:
            c.showPage()
    c.save()