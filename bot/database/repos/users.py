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
            # Сначала пытаемся получить существующего пользователя
            existing_user = await self.get(id=user.id)
            
            if existing_user:
                # Обновляем поля, включая is_admin (на случай, если статус админа изменился)
                existing_user.username = user.username or str(user.id)
                existing_user.is_admin = user.id in settings.admins
                await self.session.commit()
                logger.info(f"User updated: {existing_user}")
                return existing_user
            else:
                # Создаем нового пользователя
                new_user = await self.create(
                    id=user.id,
                    username=user.username or str(user.id),
                    is_admin=user.id in settings.admins,
                )
                await self.session.commit()
                logger.info(f"User created: {new_user}")
                return new_user
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating/updating user: {e}")
            raise

    async def get_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = select(User).where(User.id == user_id).options(*[selectinload(i) for i in user_options])

        return (await self.session.execute(q)).scalar()

    async def get_users_by_username(self, username: str) -> Sequence[User]:
        q = select(User).where(User.username == username)

        return (await self.session.execute(q)).scalars().all()
