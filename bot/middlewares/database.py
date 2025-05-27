from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable
from bot.settings import settings

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag

from bot.database import get_repo

if TYPE_CHECKING:
    from aiogram.types import TelegramObject
    from aiogram.types import User as AiogramUser

    from bot.database.engine import Repositories

IGNORED_NAMES = ["Group", "Channel"]

logger = logging.getLogger("DatabaseMiddleware")


class GetRepo(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in IGNORED_NAMES:
            return

        async with get_repo() as repo:
            data["repo"] = repo

            await handler(event, data)


class GetUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        repo: Repositories = data["repo"]
        user_: AiogramUser = data["event_from_user"]

        if user_.first_name in IGNORED_NAMES:
            return None

        user_flag = get_flag(data, "user", default=True)

        if not user_flag:
            data["user"] = None
            return await handler(event, data)

        user_options = get_flag(data, "user_options", default=[])
        user = await repo.users.get_by_user_id(user_.id, *user_options)

        if not user:
            user = await repo.users.create_from_aiogram_model(user_)
            logger.info("New user")
        else:
            user.is_admin = user_.id in settings.admins
            user.username = user_.username.lower() if user_.username else None

        data["user"] = user
        await handler(event, data)

        await repo.users.session.commit()
        return None


def setup_get_repo_middleware(dp: Dispatcher):
    """
    Setup GetRepo middleware for handlers
    :param dp:
    :return:
    """

    # default updates
    dp.message.middleware.register(GetRepo())
    dp.callback_query.middleware.register(GetRepo())
    dp.inline_query.middleware.register(GetRepo())

    # chats
    dp.my_chat_member.middleware.register(GetRepo())
    dp.chat_member.middleware.register(GetRepo())


def setup_get_user_middleware(dp: Dispatcher):
    """
    Setup GetUser middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetUser())
    dp.callback_query.middleware.register(GetUser())
    dp.inline_query.middleware.register(GetUser())

    # chats
    dp.my_chat_member.middleware.register(GetUser())
    dp.chat_member.middleware.register(GetUser())
