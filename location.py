import asyncio
import winsdk.windows.devices.geolocation as wdg
from typing import NamedTuple
from exceptions import GetLocationError

class Coordinates(NamedTuple):
    latitude: float
    longitude: float

async def _getCoords() -> Coordinates:
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return Coordinates(latitude=pos.coordinate.latitude, longitude=pos.coordinate.longitude)

def getLoc() -> Coordinates:
    try: return asyncio.run(_getCoords())
    except PermissionError: raise GetLocationError("YOU NEED TO ALLOW APPLICATIONS TO ACCESS YOU LOCATION IN SETTINGS")
    except: raise GetLocationError

    