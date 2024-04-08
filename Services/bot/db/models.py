from sqlalchemy.dialects.postgresql import INTEGER, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Reviews(Base):
    __tablename__ = "reviews"

    user_id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False)
    score: Mapped[int] = mapped_column(INTEGER, nullable=False)
    feedback: Mapped[str] = mapped_column(TEXT, nullable=False)
