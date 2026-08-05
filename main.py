from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from images2pdf import create_pdf_from_files
import os
import base64

app = FastAPI()

# Модель для приема готовых файлов
class FilePayload(BaseModel):
    filename: str
    content_base64: str

class DownloadRequest(BaseModel):
    files: List[FilePayload]

@app.post("/pdf/")
def makepdf(req: DownloadRequest):
    print(f"Получено файлов для склейки: {len(req.files)}")
    saved_files = []
    
    for f in req.files:
        try:
            # Декодируем из Base64 (отрезаем приставку "data:image/svg+xml;base64,")
            header, encoded = f.content_base64.split(",", 1)
            file_data = base64.b64decode(encoded)
            
            with open(f.filename, "wb") as out_file:
                out_file.write(file_data)
            
            saved_files.append(f.filename)
            print(f"Сохранен: {f.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении {f.filename}: {e}")

    if saved_files:
        print("Генерация PDF...")
        create_pdf_from_files(saved_files, "output.pdf")
        print("PDF готов!")
        
        # Убираем мусор
        for file in saved_files:
            if os.path.exists(file):
                os.remove(file)
                
        return {"status": "success"}
    else:
        return {"status": "error", "message": "No files saved"}
