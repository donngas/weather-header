import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy import Nominatim
from timezonefinder import TimezoneFinder

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

    def get_weather(self, latitude: float, longitude: float) -> dict:
        """
        Get weather code from Open-Meteo API.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["sunrise", "sunset"],
            "current": "weather_code",
            "timezone": self.get_timezone(latitude, longitude),
            "past_days": 1,
            "forcast_days": 1,
        }
        responses = self.weather_client.weather_api(URL, params=params)
        return responses[0]

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
