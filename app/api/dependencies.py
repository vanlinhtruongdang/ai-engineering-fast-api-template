from app.core.config import APISettings, get_settings


def get_api_settings() -> APISettings:
    return get_settings()


__all__ = ["get_api_settings"]
