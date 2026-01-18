from pydantic import BaseModel, Field
from typing import List


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
