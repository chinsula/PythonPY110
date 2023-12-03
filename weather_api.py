import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat: float, lon: float) -> dict:
    """
    Описание функции, входных и выходных переменных
    :param lat: координаты широты
    :param lon: координаты долготы
    :return: данные о погоде
    """
    token = 'fb6635df-242a-4eb2-b5eb-860b5d3ff7bd'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    result = {
        'city': data['geo_object']['locality']['name'],
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),
        'temp': data["fact"]['temp'],
        'feels_like_temp': data['fact']['feels_like'],
        'pressure': data['fact']['pressure_mm'],
        'humidity': data['fact']['humidity'],
        'wind_speed': data['fact']['wind_speed'],
        'wind_gust': data['fact']['wind_gust'],
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),
    }
    return result


if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
