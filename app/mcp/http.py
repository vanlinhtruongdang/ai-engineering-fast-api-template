import logging
import re
from secrets import compare_digest

from pydantic import SecretStr
from starlette.datastructures import Headers
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)


class BearerAuthMiddleware:
    """Protect every HTTP request to the MCP sub-application."""

    def __init__(self, app: ASGIApp, token: SecretStr) -> None:
        self.app = app
        self.token = token

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            authorization = Headers(scope=scope).getlist("authorization")
            match = (
                re.fullmatch(r"(?i:Bearer) ([A-Za-z0-9._~+/-]+=*)", authorization[0])
                if len(authorization) == 1
                else None
            )
            if match is None or not compare_digest(match[1], self.token.get_secret_value()):
                logger.warning("MCP bearer authentication rejected")
                response = JSONResponse(
                    {"detail": "Invalid bearer credentials"},
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                )
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)
