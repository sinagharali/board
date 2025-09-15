from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from database.config import database_settings as settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    future=settings.database_future,
    hide_parameters=settings.database_hide_parameters,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session_maker() as session:
        yield session
