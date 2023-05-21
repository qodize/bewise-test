import datetime
import os

os.environ["POSTGRES_USER"] = 'postgres'
os.environ["POSTGRES_PASSWORD"] = 'postgres'
os.environ["POSTGRES_SERVER"] = 'localhost'
os.environ["POSTGRES_DB"] = 'postgres'

import pytest
from fastapi.testclient import TestClient
from service_questions.app.app import app
from service_questions.app.db.database import Database
from service_questions.app.dto.create_question_dto import CreateQuestionDto
from service_questions.app.exceptions.already_exists_error import AlreadyExistsError
from service_questions.app.exceptions.bad_request_error import BadRequestError
from service_questions.app.exceptions.not_found_error import NotFoundError
from service_questions.app.repos.impl.quiz_db_repo_impl import QuizDatabaseRepo
from service_questions.app.repos.impl.quiz_find_repo_impl import JServiceQuizFindRepo
from service_questions.app.services.impl.quiz_service_impl import QuizService


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def jsquiz():
    yield JServiceQuizFindRepo()


@pytest.fixture
async def quiz_db():
    database = Database(f'postgresql+asyncpg://postgres:postgres@localhost/postgres')
    await database.drop_models()
    await database.init_models()
    yield QuizDatabaseRepo(database.session)


@pytest.fixture
def quiz_service(jsquiz, quiz_db):
    yield QuizService(jsquiz, quiz_db)


@pytest.mark.parametrize("n", [0, 1, 3, 30])
@pytest.mark.anyio()
async def test_jsquiz_find_good(n: int, jsquiz, anyio_backend):
    assert len(await jsquiz.find(n)) == n


@pytest.mark.anyio()
async def test_jsquiz_find_bad(jsquiz, anyio_backend):
    with pytest.raises(BadRequestError) as excinfo:
        await jsquiz.find(-1)
        assert isinstance(excinfo.value, BadRequestError)


@pytest.mark.parametrize("insert,get", [
    (CreateQuestionDto(id=0,
                       question='Question',
                       answer='Answer',
                       created_at=datetime.datetime.now()),
     0),
    (CreateQuestionDto(id=1231231,
                       question='asdfasdgasdf',
                       answer='asgasfgdasdfasf',
                       created_at=datetime.datetime(year=1900, month=1, day=1, hour=23)),
     1231231),
])
async def test_quiz_db_good(insert, get, quiz_db, anyio_backend):
    await quiz_db.insert_one(insert)
    assert (await quiz_db.get_one(get)).question == insert.question


@pytest.mark.parametrize("insert,get", [
    (CreateQuestionDto(id=0,
                       question='Question',
                       answer='Answer',
                       created_at=datetime.datetime.now()),
     1234123412),
    (CreateQuestionDto(id=1231231,
                       question='asdfasdgasdf',
                       answer='asgasfgdasdfasf',
                       created_at=datetime.datetime(year=1900, month=1, day=1, hour=23)),
     213123123),
])
async def test_quiz_db_bad(insert, get, quiz_db, anyio_backend):
    await quiz_db.insert_one(insert)
    with pytest.raises(NotFoundError) as excinfo:
        assert (await quiz_db.get_one(get)).question == insert.question
        assert isinstance(excinfo.value, NotFoundError)

    with pytest.raises(AlreadyExistsError) as excinfo:
        await quiz_db.insert_one(insert)
        assert isinstance(excinfo.value, AlreadyExistsError)


@pytest.mark.parametrize("insert", [
    CreateQuestionDto(id=0,
                      question='Question',
                      answer='Answer',
                      created_at=datetime.datetime.now()),
    CreateQuestionDto(id=1231231,
                      question='asdfasdgasdf',
                      answer='asgasfgdasdfasf',
                      created_at=datetime.datetime(year=1900, month=1, day=1, hour=23))
])
async def test_quiz_db_already_exists(insert, quiz_db, anyio_backend):
    await quiz_db.insert_one(insert)
    with pytest.raises(AlreadyExistsError) as excinfo:
        await quiz_db.insert_one(insert)
        assert isinstance(excinfo.value, AlreadyExistsError)


@pytest.mark.parametrize("inserts", [
    [
        CreateQuestionDto(id=0,
                          question='Question',
                          answer='Answer',
                          created_at=datetime.datetime.now()),
        CreateQuestionDto(id=1231231,
                          question='asdfasdgasdf',
                          answer='asgasfgdasdfasf',
                          created_at=datetime.datetime(year=1900, month=1, day=1, hour=23))
    ],
    [
        CreateQuestionDto(id=0,
                          question='Question',
                          answer='Answer',
                          created_at=datetime.datetime.now()),
        CreateQuestionDto(id=1,
                          question='asdfasdgasdf',
                          answer='asgasfgdasdfasf',
                          created_at=datetime.datetime(year=1900, month=1, day=1, hour=23)),
        CreateQuestionDto(id=2,
                          question='asdfasdgasdf',
                          answer='asgasfgdasdfasf',
                          created_at=datetime.datetime(year=1900, month=1, day=1, hour=23)),
        CreateQuestionDto(id=3,
                          question='asdfasdgasdf',
                          answer='asgasfgdasdfasf',
                          created_at=datetime.datetime(year=1900, month=1, day=1, hour=23)),
        CreateQuestionDto(id=4,
                          question='asdfasdgasdf',
                          answer='asgasfgdasdfasf',
                          created_at=datetime.datetime(year=1900, month=1, day=1, hour=23))
    ],
])
@pytest.mark.anyio
async def test_quiz_db_get_many(inserts, quiz_db, anyio_backend):
    for ins in inserts:
        await quiz_db.insert_one(ins)
    assert len(await quiz_db.get_many()) == len(inserts)


@pytest.mark.parametrize("n", [0, 1, 3, 30])
@pytest.mark.anyio
async def test_quiz_service_good(n, quiz_service):
    res = await quiz_service.fetch_questions(n)
    if n == 0:
        assert res is None
    else:
        assert res is not None


@pytest.mark.parametrize("n", [-1])
@pytest.mark.anyio
async def test_quiz_service_bad(n, quiz_service):
    with pytest.raises(BadRequestError) as excinfo:
        await quiz_service.fetch_questions(n)
        assert isinstance(excinfo.value, BadRequestError)


# @pytest.mark.parametrize("n", [0, 1, 2, 30])
# @pytest.mark.anyio
# async def test_quiz_endpoint_good(n, client):
#     res = client.post('/questions', json={'questions_num': n})
#
#     if n == 0:
#         assert res.json() is None
#     else:
#         assert res.json() is not None
