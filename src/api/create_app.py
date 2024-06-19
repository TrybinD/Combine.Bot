from fastapi import FastAPI

from api.data.endpoints import data_router
from api.message.endpoints import message_router


def create_app():

    app = FastAPI()
    app.include_router(data_router)
    app.include_router(message_router)

    return app
