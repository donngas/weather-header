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
            time=self._resolve_time(
                weather_data.local_time, weather_data.sunrises, weather_data.sunsets
            ),
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

    def _resolve_time(
        self, local_time: Time, sunrises: list[Time], sunsets: list[Time]
    ) -> TimeType:
        """
        Resolve time type based on local time.
        """
        # Threshold for golden hour: 25 minutes in seconds
        threshold = 25 * 60
        current_ts = local_time.raw

        # Check if within +- 25min of any sunrise or sunset
        all_events = []
        for s in sunrises:
            all_events.append((s.raw, TimeType.DAY))
            if abs(current_ts - s.raw) <= threshold:
                return TimeType.GOLDEN

        for s in sunsets:
            all_events.append((s.raw, TimeType.NIGHT))
            if abs(current_ts - s.raw) <= threshold:
                return TimeType.GOLDEN

        # Sort all events chronologically
        all_events.sort(key=lambda x: x[0])

        # Find the most recent event before current time
        # If local_time is after a sunrise but before a sunset, it returns day
        # If local_time is after a sunset but before a sunrise, it returns night
        last_event_type = None
        for ts, event_type in all_events:
            if ts <= current_ts:
                last_event_type = event_type
            else:
                break

        if last_event_type == TimeType.DAY:
            return TimeType.DAY
        elif last_event_type == TimeType.NIGHT:
            return TimeType.NIGHT

        return TimeType.DAY

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
