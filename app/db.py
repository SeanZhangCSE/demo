from typing import AsyncGenerator
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/demo")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def init_db():
    # By default we rely on Alembic migrations. For convenience in local/dev runs,
    # create tables if they don't exist.
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
