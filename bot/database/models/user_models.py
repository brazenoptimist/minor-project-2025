from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger
from .base_models import Base
from .types import str_32


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str_32] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    survey_responses: Mapped[list["SurveyResponse"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )