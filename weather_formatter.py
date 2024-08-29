from weather_api_service import Data
from config import METRIC_UNITS

def formatWeather(weather: Data) -> str:
    return f"{weather.city}: \n \
Temperature {weather.temperature}{'°C' if METRIC_UNITS else '°F'}, \n \
Weather is {weather.weather.value}, \n \
Sunrise {weather.sunrise.strftime('%H:%M')}, Sunset {weather.sunset.strftime('%H:%M')}\n"