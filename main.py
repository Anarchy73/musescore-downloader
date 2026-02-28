from curl_cffi import requests
from fastapi import FastAPI
from typing import List
from images2pdf import create_pdf_from_files
import os
app = FastAPI()

@app.post("/pdf/")
async def makepdf(srcs: List[str]):
    print(srcs)
    files = []
    for i in range(len(srcs)):
        if '.svg' in srcs[i]:
            filename = f'source_{i}.svg'
        elif '.png' in srcs[i]:
            filename = f'source_{i}.png'
        response = requests.get(srcs[i], impersonate="chrome110")
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("Файл успешно скачан!")
            files.append(filename)
        else:
            print(f"Ошибка: {response.text[:500]}")
    create_pdf_from_files(files, "output.pdf")
    for file in files:
        os.remove(file)