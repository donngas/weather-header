import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy import Nominatim
from timezonefinder import TimezoneFinder

from weather_header.calculator.schemas import WeatherData, Time
from weather_header.calculator.utils import get_local_time, convert_timestamps

URL = "https://api.open-meteo.com/v1/forecast"


class WeatherClient:
    """
    Main client for fetching weather and city name.
    """

    def __init__(self):
        # cache & retry config for openmeteo client
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        # clients
        self.weather_client = openmeteo_requests.Client(session=retry_session)
        self.geo_client = Nominatim(user_agent="weather-header")
        self.timezone_finder = TimezoneFinder()

    def get_weather(self, latitude: float, longitude: float) -> WeatherData:
        """
        Get weather code from Open-Meteo API.
        """
        timezone = self.get_timezone(latitude, longitude)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["sunrise", "sunset"],
            "current": "weather_code",
            "timezone": timezone,
            "past_days": 1,
            "forcast_days": 1,
        }
        responses = self.weather_client.weather_api(URL, params=params)
        response = responses[0]

        sunrises = []
        sunsets = []

        for sunrise in response.Daily().Variables(0).ValuesInt64AsNumpy().tolist():
            sunrise_as_time = Time(
                raw=sunrise, string=convert_timestamps([sunrise], timezone)[0]
            )
            sunrises.append(sunrise_as_time)

        for sunset in response.Daily().Variables(1).ValuesInt64AsNumpy().tolist():
            sunset_as_time = Time(
                raw=sunset, string=convert_timestamps([sunset], timezone)[0]
            )
            sunsets.append(sunset_as_time)

        ret: WeatherData = WeatherData(
            weather_code=response.Current().Variables(0).Value(),
            city=self.get_city_name(latitude, longitude),
            timezone=timezone,
            sunrises=sunrises,
            sunsets=sunsets,
            local_time=get_local_time(timezone),
        )

        return ret

    def get_city_name(self, latitude: float, longitude: float) -> str:
        """
        Get city name from coordinates.
        """
        location = self.geo_client.reverse(f"{latitude}, {longitude}", exactly_one=True)
        # TODO: handle cases where there might be no city key.
        return location.raw["address"]["city"]

    def get_timezone(self, latitude: float, longitude: float) -> str:
        """
        Get timezone from coordinates.
        """
        return self.timezone_finder.timezone_at(lat=latitude, lng=longitude)
