import uvicorn

from app import create_app


app = create_app()


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
