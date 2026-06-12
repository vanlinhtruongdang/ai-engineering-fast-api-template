from httpx import ASGITransport, AsyncClient

from app.main import app


async def request(method: str, path: str, headers: dict[str, str] | None = None):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, headers=headers)


async def get(path: str):
    return await request("GET", path)


async def test_health_check() -> None:
    response = await get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_root_health_check() -> None:
    response = await get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_system_info_root() -> None:
    response = await get("/api/v1/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "name": "FastAPI Template",
        "version": "0.1.0",
        "environment": "development",
    }


async def test_scalar_docs() -> None:
    response = await get("/scalar")

    assert response.status_code == 200


async def test_swagger_docs() -> None:
    response = await get("/docs")

    assert response.status_code == 200


async def test_cors_allows_browser_requests() -> None:
    response = await request(
        "GET",
        "/api/v1/health",
        headers={"Origin": "http://localhost:3000"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
