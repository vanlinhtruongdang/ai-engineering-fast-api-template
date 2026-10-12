from app.core.config import get_settings
from app.core.logging import configure_logging
from app.mcp import create_server


def main() -> None:
    configure_logging()
    create_server(get_settings()).run("stdio")


if __name__ == "__main__":
    main()
