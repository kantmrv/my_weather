import json
import ssl
import urllib.request
from typing import NamedTuple, Literal
from datetime import datetime
from enum import StrEnum
from json.decoder import JSONDecodeError
from urllib.error import URLError

from config import ROUND_COORDINATES, OPENWEATHER_API, OPENWEATHER_URL, METRIC_UNITS
from location import Coordinates
from exceptions import ApiServerError

class WeatherType(StrEnum):
    Thunderstorm: str = "Thunderstorm"
    Drizzle: str = "Drizzle"
    Rain: str = "Rain"
    Snow: str = "Snow"
    Atmosphere: str = "Atmosphere"
    Clear: str = "Clear"
    Clouds: str = "Clouds"

class Units(StrEnum):
    Metric: str = "metric"
    Imperial: str = "imperial"

class Data(NamedTuple):
    temperature: float
    weather: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str

def getWeather(coordinates: Coordinates) -> Data:
    openweather_response: str = _get_openweather_response(latitude = coordinates.latitude, longitude = coordinates.longitude)
    data: Data = _parse_openweather_response(openweather_response)
    return data

def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url: str = OPENWEATHER_URL.format(lat = latitude, lon = longitude, api = OPENWEATHER_API, units = Units.Metric if METRIC_UNITS else Units.Imperial)
    try: return urllib.request.urlopen(url).read()
    except URLError: raise ApiServerError("URL OPENWEATHER ERROR")

def _parse_openweather_response(openweather_response: str) -> Data:
    try: openweather_dict = json.loads(openweather_response)
    except JSONDecodeError: raise ApiServerError("JSON DECODE ERROR")
    return Data(
        temperature = _parse_temperature(openweather_dict),
        weather = _parse_weather_type(openweather_dict),
        sunrise = _parse_sun_time(openweather_dict, "sunrise"),
        sunset = _parse_sun_time(openweather_dict, "sunset"),
        city = _parse_city(openweather_dict),
    )

def _parse_temperature(openweather_dict: dict) -> float:
    return round(openweather_dict["main"]["temp"]) if ROUND_COORDINATES else openweather_dict["main"]["temp"]

def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try: weathert_type_id: str = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError): raise ApiServerError("PARSE WEATHER TYPE ERROR")
    weathert_types = {
        "1": WeatherType.Thunderstorm,
        "3": WeatherType.Drizzle,
        "5": WeatherType.Rain,
        "6": WeatherType.Snow,
        "7": WeatherType.Atmosphere,
        "800": WeatherType.Clear,
        "80": WeatherType.Clouds,
    }
    for _id, _weather_type in weathert_types.items():
        if weathert_type_id.startswith(_id): return _weather_type
    raise ApiServerError("WEATHER TYPES ERROR")

def _parse_sun_time(openweather_dict: dict, time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])

def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict["name"]