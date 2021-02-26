from fastapi import FastAPI
import uvicorn

from routers import video


app = FastAPI()
app.include_router(video.router)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
