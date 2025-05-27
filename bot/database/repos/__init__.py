from __future__ import annotations

from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from .users import UsersRepo
from .survey_response import SurveyResponseRepo


@dataclass
class Repositories:
    session: AsyncSession
    users: UsersRepo
    survey_responses: SurveyResponseRepo

    @staticmethod
    def get_repo(session: AsyncSession) -> Repositories:
        return Repositories(session=session, users=UsersRepo(session), survey_responses=SurveyResponseRepo(session))


__all__ = [
    "Repositories",
]
