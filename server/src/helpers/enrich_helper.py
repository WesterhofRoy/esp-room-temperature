import datetime as dt
import requests
from src.models.esp_data import EspData
from src.models.enriched_data import EnrichedData, WeatherData
from src.config import settings


def convert_time_to_epoch(date: dt.date, time: dt.time) -> int:
    return int(dt.datetime.combine(date, time).timestamp())


def fetch_weather_data(timestamp: int):
    # Get current time (UTC)
    baseUrl = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={settings.LAT}&lon={settings.LON}&units={settings.UNITS}&appid={settings.API_KEY}'
    request_url = f'{baseUrl}&dt={timestamp}'
    response = requests.get(request_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f'Error fetching weather data: {response.status_code}\n{response.text}')


def getDateTime(date: dt.date, time: str) -> str:
    time = dt.datetime.strptime(time, '%H:%M:%S').time()
    return f'{date} {time}'


def getEpochTime(dateTime: str) -> int:
    return int(dt.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S').timestamp())


def getRoomActivity(dateTime: str) -> str:
    time = dt.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S').time()
    # Between 0000 and 0930, roomActivity is sleeping
    if time < dt.time(9, 30):
        return 'sleeping'
    # Between 0930 and 1700, roomActivity is working
    elif time < dt.time(17, 0):
        return 'working'
    # Between 1700 and 1900, roomActivity is unoccupied
    elif time < dt.time(19, 0):
        return 'unoccupied'
    # Between 1900 and 0000, roomActivity is hobbies
    elif time < dt.time(0, 0):
        return 'hobbies'
    # Exhastive activity
    else:
        return 'unknown'


def getWeatherData(timestamp: str) -> WeatherData:
    weather_data = fetch_weather_data(timestamp)
    return WeatherData(
        temperature=weather_data['data'][0]['temp'],
        condition=weather_data['data'][0]['weather'][0]['description']
    )


def enrichEspData(data: EspData) -> EnrichedData:
    datetime = getDateTime(data.date, data.time)
    timestamp = getEpochTime(datetime)
    roomActivity = getRoomActivity(datetime)
    weather = getWeatherData(timestamp)
    return EnrichedData(
        timestamp=timestamp,
        datetime=datetime,
        temperature=data.temperature,
        roomActivity=roomActivity,
        weather=weather
    )
