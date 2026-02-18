from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

drawing = svg2rlg("aboba.svg")
drawing.add(svg2rlg("aboba.svg"))
renderPDF.drawToFile(drawing, "output_file.pdf")
