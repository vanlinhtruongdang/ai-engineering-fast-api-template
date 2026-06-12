from app.services import get_health_status


def test_get_health_status() -> None:
    payload = get_health_status()

    assert payload.status == "ok"
