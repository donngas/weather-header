from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    is_free_tier: bool

    is_frame_custom: bool = Field(default=False)
    frame_name: str = Field(default="default")

    is_texture_custom: bool = Field(default=False)
    texture_name: str = Field(default="default")
