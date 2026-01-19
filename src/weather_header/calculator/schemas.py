from pydantic import BaseModel, Field
from typing import List
from enum import Enum


# Pydantic models for DTO between WeatherClient and StateResolver


class Time(BaseModel):
    """
    Time class that covers both int timestamp and parsed string.
    """

    raw: int
    string: str


class WeatherData(BaseModel):
    """
    Parsed weather data DTO to be passed between WeatherClient and StateResolver.
    """

    weather_code: int = Field(..., validation_alias="weather_code")
    city: str = Field(default="Unknown")
    timezone: str = Field(default="Unknown")

    sunrises: List[Time]
    sunsets: List[Time]
    local_time: Time


# Pydantic models for StateResolver results


class WeatherType(str, Enum):
    """
    Enum for weather types.
    """

    SUNNY = "sunny"
    OVERCAST = "overcast"
    RAIN = "rain"
    SNOW = "snow"


class TimeType(str, Enum):
    """
    Enum for time types.
    """

    DAY = "day"
    NIGHT = "night"
    GOLDEN = "golden"


class UserState(BaseModel):
    """
    Class for resolved final weather information for user.
    """

    weather: WeatherType
    time: TimeType

    # to determine heaviness of rain or weather
    is_heavy: bool

    # to determine lightning effects
    is_storm: bool
