import uvicorn

from app import create_app


app = create_app()


@app.on_event("startup")
async def init_db():
    await app.db.init_connection_pool()
    await app.db.init_table()


def main() -> None:

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )


if __name__ == '__main__':
    main()
