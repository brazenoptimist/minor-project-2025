from __future__ import annotations

from typing import Sequence
import logging
from bot.filters import IsAdmin
from aiogram.types import User as AiogramUser
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from bot.settings import settings

from .base import BaseRepo
from bot.database.models import User

logger = logging.getLogger(__name__)


class UsersRepo(BaseRepo):
    model = User

    async def create_from_aiogram_model(self, user: AiogramUser) -> User:
        try:
            us = await self.create(
                id=user.id,
                username=user.username or str(user.id)
            )
            await self.session.commit()  # Явный коммит
            logger.info(f"User created: {us}")
            return us
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating user: {e}")
            raise

    async def get_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = select(User).where(User.id == user_id).options(*[selectinload(i) for i in user_options])

        return (await self.session.execute(q)).scalar()

    async def get_users_by_username(self, username: str) -> Sequence[User]:
        q = select(User).where(User.username == username)

        return (await self.session.execute(q)).scalars().all()
