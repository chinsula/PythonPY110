import requests

key = "fb6635df-242a-4eb2-b5eb-860b5d3ff7bd"  # TODO подставьте значение вашего ключа доступа к API
lat = "59.93"  # широта в градусах
lon = "30.31"  # долгота в градусах

url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
headers={"X-Yandex-API-Key": f"{key}"}

response = requests.get(url, headers=headers)
print(response.json())