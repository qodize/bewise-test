from fastapi import FastAPI

from service_questions.app.di.containers import Container
from service_questions.app.routers import quiz_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(quiz_router.router)

    container = Container()
    app.container = container

    @app.on_event('startup')
    async def startup():
        await app.container.db().init_models()

    return app


app = create_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
