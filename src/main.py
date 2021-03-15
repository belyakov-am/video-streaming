from fastapi import FastAPI
import uvicorn

from routers import video
from utils import init_video_dir


app = FastAPI()
app.include_router(video.router)


def main() -> None:
    init_video_dir()

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )


if __name__ == '__main__':
    main()
