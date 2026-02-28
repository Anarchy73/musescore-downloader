from curl_cffi import requests
from fastapi import FastAPI
from typing import List
from images2pdf import create_pdf_from_files
app = FastAPI()

@app.post("/pdf/")
async def makepdf(srcs: List[str]):
    print(srcs)
    files = []
    for i in range(len(srcs)):
        filename = f'source_{i}.svg'
        response = requests.get(srcs[i], impersonate="chrome110")
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("Файл успешно скачан!")
        else:
            print(f"Ошибка: {response.text[:500]}")
        files.append(filename)
    create_pdf_from_files(files, "output.pdf")