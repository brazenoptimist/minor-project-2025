from sqlalchemy import ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base_models import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Основные данные
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    course: Mapped[str] = mapped_column(nullable=True)
    gpa: Mapped[float] = mapped_column(nullable=True)
    stress_level: Mapped[int] = mapped_column(nullable=True)
    anxiety_score: Mapped[int] = mapped_column(nullable=True)
    sleep_quality: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    physical_activity: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str

    diet_quality: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    social_support: Mapped[str] = mapped_column(nullable=True)
    relationship_status: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    substance_use: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    counseling_service_use: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    family_history: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    chronic_illness: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    financial_stress: Mapped[int] = mapped_column(nullable=True)
    extracurricular_involvement: Mapped[str] = mapped_column(nullable=True)
    semester_credit_load: Mapped[int] = mapped_column(nullable=True)
    residence_type: Mapped[str] = mapped_column(nullable=True)  # изменено с int на str
    bot_rating: Mapped[int] = mapped_column(nullable=True)

    # Связь с пользователем
    user: Mapped["User"] = relationship(back_populates="survey_responses")
