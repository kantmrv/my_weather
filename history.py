from datetime import datetime
from pathlib import Path
from weather_api_service import Data

from weather_api_service import Data
from weather_formatter import formatWeather

class WeatherStorage:
    def save(self, weather: Data) -> None:
        raise NotImplementedError
    
class PlainFileWeatherStorage(WeatherStorage):
    def __init__(self, file: Path) -> None:
        self._file: Path = file
    def save(self, weather: Data) -> None:
        now: datetime = datetime.now()
        formatted_weather: str = formatWeather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now}\n{formatted_weather}\n")

def save_weather(weather: Data, storage: WeatherStorage) -> None:
    storage.save(weather)