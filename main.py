from curl_cffi import requests

url = "https://musescore.com/static/musescore/scoredata/g/92c16cc6229b458981463c3ddb37bec8f1b43888/score_0.svg"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://musescore.com/',
}

# Используем impersonate для имитации браузера
response = requests.get(url, headers=headers, impersonate="chrome110")

print(f"Статус код: {response.status_code}")

if response.status_code == 200:
    with open('aboba.svg', 'wb') as f:
        f.write(response.content)
    print("Файл успешно скачан!")
    
    # Проверим содержание
    print(f"Начало файла: {response.content[:50]}")
else:
    print(f"Ошибка: {response.text[:500]}")
