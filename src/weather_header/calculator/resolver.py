from weather_header.calculator.schemas import (
    WeatherData,
    UserState,
    WeatherType,
    TimeType,
    Time,
)


class StateResolver:
    _WEATHER_MAPPING = {
        WeatherType.OVERCAST: [range(2, 50)],
        WeatherType.RAIN: [range(50, 71), range(80, 84), range(91, 93), range(95, 100)],
        WeatherType.SNOW: [range(70, 80), range(85, 91), range(93, 95)],
    }

    def __init__(self):
        pass

    def resolve(self, weather_data: WeatherData) -> UserState:
        """
        Resolve the weather data into a UserState object.
        """
        return UserState(
            weather=self._resolve_weather(weather_data.weather_code),
            time=self._resolve_time(weather_data.local_time),
            is_heavy=self._resolve_is_heavy(weather_data.weather_code),
            is_storm=self._resolve_is_storm(weather_data.weather_code),
        )

    def _resolve_weather(self, weather_code: int) -> WeatherType:
        """
        Resolve weather type based on weather code.
        """
        for weather_type, code_ranges in self._WEATHER_MAPPING.items():
            if any(weather_code in code_range for code_range in code_ranges):
                return weather_type

        return WeatherType.SUNNY

    def _resolve_time(self, local_time: Time) -> TimeType:
        """
        Resolve time type based on local time.
        """
        pass

    def _resolve_is_heavy(self, weather_code: int) -> bool:
        """
        Resolve if the weather is heavy based on the weather code.
        """
        return weather_code in [82, 65, 75, 99]

    def _resolve_is_storm(self, weather_code: int) -> bool:
        """
        Resolve if the weather is storm based on the weather code.
        """
        return weather_code in range(95, 100)
