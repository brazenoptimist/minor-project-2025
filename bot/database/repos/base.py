# mypy: ignore-errors

from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any, Sequence, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from bot.database.models.base_models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


Model = TypeVar("Model", bound=Base)


class BaseRepo(ABC):
    model: Base

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        if self.model is None:
            msg = "It is necessary to define the 'model' attribute in the descendant class."
            raise NotImplementedError(msg)

    async def create(self, **kwargs: dict[str, Any]) -> Model:
        db_obj: Model = self.model(**kwargs)
        return await self.create_from_model(db_obj)

    async def create_from_model(self, *db_obj: Model) -> Model | tuple[Model]:
        for i in db_obj:
            self.session.add(i)

        await self.session.commit()

        return db_obj[0] if len(db_obj) == 1 else db_obj

    async def get(self, *args, **filters) -> Model | None:
        if args and not filters:
            if hasattr(self.model, 'id'):
                filters = {'id': args[0]}
            else:
                raise ValueError("Model has no 'id' attribute to filter by")
        
        q = select(self.model).filter_by(**filters)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def delete(self, *db_objects: Model) -> None:
        for i in db_objects:
            await self.session.delete(i)
        await self.session.commit()

    async def update(self, db_object: Model) -> None:
        self.session.add(db_object)
        await self.session.commit()

        # await self.session.refresh(db_object)
        # return db_object
        return

    async def get_all(self, *, count: bool = False) -> int | Sequence[Model]:
        if count:
            stmt = select(func.count()).select_from(self.model)
            result = await self.session.execute(stmt)
            return result.scalar_one()

        result = await self.session.execute(select(self.model))
        return result.scalars().all()
