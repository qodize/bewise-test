import datetime

from service_questions.app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func


class QuestionModel(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str]
    answer: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
