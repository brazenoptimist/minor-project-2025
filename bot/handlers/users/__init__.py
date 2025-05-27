from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start_help, survey

routers: list[Router] = [start_help.router, survey.router]

_all__ = ["routers"]
