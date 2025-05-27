import logging

from aiogram import Dispatcher
from .database import setup_get_repo_middleware, setup_get_user_middleware
from .throttling import setup_throttling_middleware
logger = logging.getLogger("middlewares")


def setup_middlewares(dp: Dispatcher) -> None:
    logger.info("Setting up middlewares...")
    setup_throttling_middleware(dp)
    setup_get_repo_middleware(dp)
    setup_get_user_middleware(dp)
    logger.info("Middlewares setup complete")
    logger.debug("middlewares was been load")


__all__ = ["setup_middlewares"]