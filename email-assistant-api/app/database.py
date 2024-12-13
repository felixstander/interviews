"""
创建应用程序并设置数据库
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite+aiosqlite:///./emailassistant.db"
engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
