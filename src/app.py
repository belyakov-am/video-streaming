import os

from fastapi import FastAPI

from db.manager import DBManager
from routers import video, root


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(video.router)
    app.add_api_route("/", root.root)

    setup_db(app)

    return app


def setup_db(app: FastAPI) -> None:
    app.db = DBManager(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        db=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
