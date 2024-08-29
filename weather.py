from pathlib import Path

from location import getLoc
from weather_api_service import getWeather
from weather_formatter import formatWeather
from history import save_weather, PlainFileWeatherStorage
from exceptions import *


def main():
    try: 
        coordinates = getLoc()
        weather = getWeather(coordinates)
        print(formatWeather(weather))
        save_weather(weather, PlainFileWeatherStorage(Path.cwd() / "history.txt"))
    except GetLocationError: print("PROGRAM CANT GET CURRENT GPS")
    except ApiServerError: print("PROGRAM CANT GET CURRENT WEATHER")


if __name__ == "__main__":
    main()