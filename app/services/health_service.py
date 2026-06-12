from app.schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")


__all__ = ["get_health_status"]
