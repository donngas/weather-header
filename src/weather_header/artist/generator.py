import base64
from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader


class SVGGenerator:
    def __init__(self, assets_path: Path, templates_path: Path):
        self.assets_path = assets_path
        self.env = Environment(loader=FileSystemLoader(templates_path))

    def render(self, state, user_pref) -> str:
        """
        Generates the final SVG string by building context and rendering the template.
        """
        context = self.build_context(state, user_pref)
        template = self.env.get_template("svg/view.svg")
        return template.render(**context)

    def _get_base64(
        self,
        type: Literal["sprite", "frame", "texture"],
        weather_state: str | None = None,
        frame_name: str | None = None,
        texture_name: str | None = None,
    ) -> str:
        # find the right file
        names = {"sprite": weather_state, "frame": frame_name, "texture": texture_name}

        # map type to folder name (plural)
        folders = {"sprite": "sprites", "frame": "frames", "texture": "textures"}

        file_path = self.assets_path / folders[type] / f"{names[type]}.png"

        # read the binary data and encode it
        with open(file_path, "rb") as f:
            binary_data = f.read()
            base64_data = base64.b64encode(binary_data).decode("utf-8")

        return base64_data

    def build_context(self, state, user_pref) -> dict:
        # create the dictionary for Jinja
        # TODO: sprite_str should also handle day and night, as current plan is to have separate sprite files for them

        # Resolve frame and texture
        frame_name = user_pref.frame_name if user_pref.is_frame_custom else "default"
        texture_name = (
            user_pref.texture_name if user_pref.is_texture_custom else "default"
        )

        sprite_str = self._get_base64("sprite", weather_state=f"{state.weather}")
        frame_str = self._get_base64("frame", frame_name=frame_name)
        texture_str = self._get_base64("texture", texture_name=texture_name)

        # Animation constants
        frame_width = 300
        frame_height = 200
        frame_count = 12  # Assumed default
        total_width = frame_width * frame_count
        animation_x = 500
        animation_y = 0

        return {
            "base64_sprite": sprite_str,
            "base64_frame": frame_str,
            "base64_texture": texture_str,
            "bg_color": "#2C3E50" if state.time == "night" else "#87CEEB",
            # Animation Geometry
            "animation_width": frame_width,
            "animation_height": frame_height,
            "animation_x": animation_x,
            "animation_y": animation_y,
            "total_animation_width": total_width,
            "frame_count": frame_count,
            "duration": 2,
            "show_watermark": user_pref.is_free_tier,
        }
