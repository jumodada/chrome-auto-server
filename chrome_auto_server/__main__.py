import uvicorn

from chrome_auto_server.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "chrome_auto_server.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
