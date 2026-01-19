import base64
from pathlib import Path


class SVGGenerator:
    def __init__(self, assets_path: Path):
        self.assets_path = assets_path

    def _get_base64_sprite(self, weather_state: str) -> str:
        # find the right file
        file_path = self.assets_path / f"{weather_state}.png"

        # read the binary data and encode it
        with open(file_path, "rb") as f:
            binary_data = f.read()
            base64_data = base64.b64encode(binary_data).decode("utf-8")

        return base64_data

    def build_context(self, state, user_pref):
        # create the dictionary for Jinja
        sprite_str = self._get_base64_sprite(f"{state.weather}_{state.is_heavy}")

        return {
            "base64_content": sprite_str,
            "bg_color": "#2C3E50" if state.time == "night" else "#87CEEB",
            "total_width": 1200,  # (Frame Width * Total Frames)
            "frame_width": 100,  # Width of one single frame
            "frame_count": 12,
            "duration": 1,  # 1 second for the whole loop
            "show_watermark": user_pref.is_free_tier,
        }
