from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from weather_header.calculator.schemas import Time


def get_local_time(tz_string: str) -> Time:
    """
    Get local time from timezone string.
    """
    return Time(
        raw=datetime.now(ZoneInfo(tz_string)),
        string=datetime.now(ZoneInfo(tz_string)).strftime("%Y-%m-%dT%H:%M"),
    )


def convert_timestamps(timestamps: list[int], tz_string: str) -> list[str]:
    """
    Converts Unix timestamps to local ISO strings using IANA timezone names.
    """
    local_tz = ZoneInfo(tz_string)
    iso_strings = []

    for ts in timestamps:
        # Create UTC datetime & convert to the target local timezone
        dt_local = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(local_tz)

        # Format to ISO
        iso_strings.append(dt_local.strftime("%Y-%m-%dT%H:%M"))

    return iso_strings
