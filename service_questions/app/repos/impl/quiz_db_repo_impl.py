import typing
import contextlib

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from service_questions.app.db.models.question_model import QuestionModel
from service_questions.app.dto.create_question_dto import CreateQuestionDto
from service_questions.app.dto.question_dto import QuestionDto
from service_questions.app.exceptions.already_exists_error import AlreadyExistsError
from service_questions.app.exceptions.not_found_error import NotFoundError
from service_questions.app.repos.abstract.quiz_db_repo_abc import QuizDatabaseRepoABC


class QuizDatabaseRepo(QuizDatabaseRepoABC):
    def __init__(self, session_factory: typing.Callable[..., contextlib.AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def insert_one(self, create_question: CreateQuestionDto) -> None:
        async with self.session_factory() as session:
            question = QuestionModel(
                id=create_question.id,
                question=create_question.question,
                answer=create_question.answer,
                created_at=create_question.created_at
            )
            session.add(question)
            try:
                await session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                raise AlreadyExistsError()

    async def get_one(self, question_id: int) -> QuestionDto:
        async with self.session_factory() as session:
            result = (await session.execute(select(QuestionModel).filter(QuestionModel.id == question_id)))
            question = result.scalars().first()
            if question is None:
                raise NotFoundError()
            return question

    async def get_many(self) -> list[QuestionDto]:
        async with self.session_factory() as sesssion:
            result = await sesssion.execute(select(QuestionModel))
            return [q for q in result.scalars()]
