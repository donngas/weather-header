from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from weather_header.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # Preferences
    is_free_tier: Mapped[bool] = mapped_column(Boolean, default=True)

    is_frame_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    frame_name: Mapped[str] = mapped_column(String(50), default="default")

    is_texture_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    texture_name: Mapped[str] = mapped_column(String(50), default="default")
