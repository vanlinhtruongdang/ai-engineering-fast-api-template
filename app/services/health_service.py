from app.schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")


def get_readiness_status() -> HealthResponse:
    """Return readiness for the dependency-free template baseline."""

    return HealthResponse(status="ok")


__all__ = ["get_health_status", "get_readiness_status"]
