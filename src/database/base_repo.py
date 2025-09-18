from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get(self, model: type[T], id_: UUID) -> T | None:
        stmt = select(model).where(model.id_ == id_)
        result = await self.db_session.exec(stmt)
        return result.one_or_none()

    async def create(self, obj: T) -> T:
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def update(self, obj: T) -> T:
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        self.db_session.delete(obj)
        await self.db_session.commit()
