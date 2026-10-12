from mcp.server import MCPServer
from mcp_types import ToolAnnotations

from app.core.config import APISettings
from app.schemas.health import HealthResponse
from app.services import get_health_status
from app.services.info_service import get_system_info


def create_server(settings: APISettings) -> MCPServer:
    server = MCPServer(settings.app_name, version=settings.app_version, subscriptions=False)

    @server.tool(
        name="get_health_status",
        annotations=ToolAnnotations(
            read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False
        ),
    )
    async def health_status() -> HealthResponse:
        """Read the dependency-free application liveness status."""
        return get_health_status()

    @server.resource("app://info", mime_type="application/json")
    async def application_info() -> str:
        """Read application name, version, environment and baseline status."""
        return get_system_info(settings).model_dump_json()

    return server
