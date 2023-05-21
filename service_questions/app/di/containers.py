import os

from dependency_injector import containers, providers

from service_questions.app.db.database import Database
from service_questions.app.repos.impl.quiz_db_repo_impl import QuizDatabaseRepo
from service_questions.app.repos.impl.quiz_find_repo_impl import JServiceQuizFindRepo
from service_questions.app.services.impl.quiz_service_impl import QuizService


class Container:
    wiring_config = containers.WiringConfiguration(modules=["service_questions.app.routers"])

    db = providers.Singleton(
        Database,
        f'postgresql+asyncpg://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_SERVER"]}/{os.environ["POSTGRES_DB"]}'
    )

    quiz_db_repo = providers.Factory(
        QuizDatabaseRepo,
        session_factory=db.provided.session
    )

    quiz_find_repo = providers.Factory(
        JServiceQuizFindRepo
    )

    quiz_service = providers.Factory(
        QuizService,
        quiz_db_repo=quiz_db_repo,
        quiz_find_repo=quiz_find_repo
    )
