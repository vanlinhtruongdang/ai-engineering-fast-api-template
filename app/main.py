import uvicorn
from fastapi import FastAPI

from app.api.app import create_app
from app.core import get_settings

app: FastAPI = create_app()


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.server_reload,
        reload_excludes=["logs/*", "*.log", ".venv/*", "dist/*", "build/*"],
    )


if __name__ == "__main__":
    run()


__all__ = ["app", "run"]
