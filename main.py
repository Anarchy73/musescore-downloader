from curl_cffi import requests
from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.post("/pdf/")
async def makepdf(srcs: List[str]):
  print(srcs)
  for i in range(len(srcs)):
    response = requests.get(srcs[i], impersonate="chrome110")
    if response.status_code == 200:
        with open(f'source_{i}.svg', 'wb') as f:
            f.write(response.content)
        print("Файл успешно скачан!")
    else:
        print(f"Ошибка: {response.text[:500]}")