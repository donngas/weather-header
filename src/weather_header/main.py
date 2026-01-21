import os
from pathlib import Path
from types import SimpleNamespace

from fastapi import FastAPI, Response

from .artist.generator import SVGGenerator

app = FastAPI()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


@app.get("/")
def read_root():
    return {"Hello": "World"}


if DEBUG:

    @app.get("/debug/view")
    def debug_view():
        assets_path = Path(__file__).parent / "static"
        templates_path = Path(__file__).parent / "templates"
        generator = SVGGenerator(assets_path, templates_path)

        # Mock objects
        # state needs .weather and .time
        state = SimpleNamespace(weather="debug_sprite", time="day")
        # user_pref needs .is_frame_custom, .frame_name, .is_texture_custom, .texture_name, .is_free_tier
        user_pref = SimpleNamespace(
            is_frame_custom=True,
            frame_name="full_window",
            is_texture_custom=True,
            texture_name="creamwhite_full_window",
            is_free_tier=True,  # Show watermark for debug
        )

        svg = generator.render(state, user_pref)
        return Response(content=svg, media_type="image/svg+xml")
