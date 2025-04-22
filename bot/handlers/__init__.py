from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Dispatcher

logger = logging.getLogger("handlers")

def setup_routers(dp: Dispatcher) -> None:
    from . import admins, users

    all_routers = [*users.routers, *admins.routers]
    dp.include_routers(*all_routers)

    logger.debug("%s routers have been loaded", len(all_routers))

__all__ = [
    "setup_routers",
]
