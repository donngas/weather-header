from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_header.users.models import User
from weather_header.users.schemas import UserPreferences


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def to_preferences_dto(self, user: User) -> UserPreferences:
        return UserPreferences(
            is_free_tier=user.is_free_tier,
            is_frame_custom=user.is_frame_custom,
            frame_name=user.frame_name,
            is_texture_custom=user.is_texture_custom,
            texture_name=user.texture_name,
        )

    async def get_preferences(self, user_id: int) -> Optional[UserPreferences]:
        user = await self.get_by_id(user_id)
        if user:
            return self.to_preferences_dto(user)
        return None

    async def create_user(self, username: str) -> User:
        user = User(username=username)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_preferences(self, user: User, prefs: UserPreferences) -> User:
        user.is_free_tier = prefs.is_free_tier
        user.is_frame_custom = prefs.is_frame_custom
        user.frame_name = prefs.frame_name
        user.is_texture_custom = prefs.is_texture_custom
        user.texture_name = prefs.texture_name

        await self.session.commit()
        await self.session.refresh(user)
        return user
