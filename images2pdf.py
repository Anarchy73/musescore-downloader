from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_pdf_from_files(files, output_file):
    # Создаем холст PDF
    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4
    
    for i, img in enumerate(files):
        print(f"Добавляю в PDF страницу {i+1} из {len(files)}...")
        
        if img.endswith('.svg'):
            drawing = svg2rlg(img)
            if drawing:
                # Высчитываем пропорции, чтобы ноты влезли на лист А4
                aspect = min(page_width / drawing.width, page_height / drawing.height)
                drawing.scale(aspect, aspect)
                
                # Рисуем векторную графику
                renderPDF.draw(drawing, c, 0, 0)
                
        elif img.endswith('.png'):
            # preserveAspectRatio=True гарантирует, что картинка не сплющится
            c.drawImage(img, 0, 0, width=page_width, height=page_height, preserveAspectRatio=True, anchor='c')
            
        # БЕЗУСЛОВНО закрываем текущую страницу и создаем чистый лист для следующей.
        # ReportLab достаточно умен, чтобы не добавлять пустую страницу в самом конце.
        c.showPage()
        
    # Сохраняем итоговый документ
    c.save()
    print("Генерация PDF завершена!")
