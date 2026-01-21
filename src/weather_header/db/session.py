import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to local default if not set (helpful for simple testing/verification without docker)
    # But ideally should raise error in production.
    # For now, let's just let it be required.
    pass


if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create Async Engine for application use
engine = create_async_engine(DATABASE_URL, echo=False)

# Create Session Factory
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    print("--- init_db started ---")
    # Import models explicitly to register them with Base.metadata
    from weather_header.users.models import User

    print(f"User class: {User}")
    print(f"User.__tablename__: {User.__tablename__}")
    print(f"User.__table__: {User.__table__}")

    # Use the metadata from the model itself to ensure we have the right registry
    metadata = User.metadata

    print(f"Tables to create: {metadata.tables.keys()}")

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    print("--- init_db finished ---")
