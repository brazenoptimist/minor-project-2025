
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.survey_response_models import SurveyResponse


class SurveyResponseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        age: int,
        gender: str,
        **additional_fields
    ) -> SurveyResponse:
        response = SurveyResponse(
            user_id=user_id,
            age=age,
            gender=gender,
            **additional_fields
        )
        self.session.add(response)
        return response

    async def get_by_user(self, user_id: int) -> list[SurveyResponse]:
        result = await self.session.execute(
            select(SurveyResponse)
            .where(SurveyResponse.user_id == user_id)
        )
        return result.scalars().all()

    async def get_last_by_user(self, user_id: int) -> SurveyResponse | None:
        result = await self.session.execute(
            select(SurveyResponse)
            .where(SurveyResponse.user_id == user_id)
            .order_by(SurveyResponse.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_user_responses(self, user_id: int) -> list[SurveyResponse]:
        result = await self.session.execute(
            select(SurveyResponse)
            .where(SurveyResponse.user_id == user_id)
            .order_by(SurveyResponse.created_at.desc())
        )
        return result.scalars().all()

    async def delete_response(self, response_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            delete(SurveyResponse)
            .where(
                SurveyResponse.id == response_id,
                SurveyResponse.user_id == user_id
            )
            .returning(SurveyResponse.id)
        )
        await self.session.commit()
        return bool(result.scalar())
    
    async def get_by_id(self, response_id: int) -> SurveyResponse | None:
        result = await self.session.execute(
            select(SurveyResponse)
            .where(SurveyResponse.id == response_id)
        )
        return result.scalar_one_or_none()