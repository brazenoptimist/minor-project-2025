from sqlalchemy.orm import mapped_column, Mapped
from .base_models import Base
from .types import str_32


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str_32] = mapped_column(nullable=False)
