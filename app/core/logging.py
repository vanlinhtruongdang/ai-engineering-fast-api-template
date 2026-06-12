import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

from app.core.config import get_logging_settings

_LOGGING_CONFIGURED = False


def configure_logging() -> None:
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    settings = get_logging_settings()
    log_dir = Path(settings.dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(settings.level.upper())
    root.handlers.clear()
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s | %(asctime)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    file_formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)

    rotating_file = RotatingFileHandler(
        log_dir / settings.file,
        maxBytes=settings.max_bytes,
        backupCount=settings.backup_count,
        encoding="utf-8",
    )
    rotating_file.setFormatter(file_formatter)
    root.addHandler(rotating_file)

    _LOGGING_CONFIGURED = True


__all__ = ["configure_logging"]
