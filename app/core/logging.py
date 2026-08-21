import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

from app.core.config import get_logging_settings

_LOGGING_CONFIGURED = False


class JsonFormatter(logging.Formatter):
    """Render standard log records as single-line JSON without external dependencies."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
        )


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

    console_formatter: logging.Formatter = colorlog.ColoredFormatter(
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
    if settings.json_logs:
        console_formatter = JsonFormatter()

    file_formatter: logging.Formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if settings.json_logs:
        file_formatter = JsonFormatter()

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
