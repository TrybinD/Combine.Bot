from fastapi import FastAPI

from api.data.endpoints import data_router


def create_app():

    app = FastAPI()
    app.include_router(data_router)

    return app
