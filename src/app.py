from fastapi import FastAPI

from routers import video
from utils import init_video_dir


def create_app() -> FastAPI:
    init_video_dir()

    app = FastAPI()
    app.include_router(video.router)

    return app
