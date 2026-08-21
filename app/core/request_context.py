from uuid import uuid4

from fastapi import Request, Response


async def attach_request_id(request: Request, call_next) -> Response:
    """Attach a correlation identifier without trusting an empty client value."""

    header_name = request.app.state.request_id_header
    request_id = request.headers.get(header_name) or str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers[header_name] = request_id
    return response


__all__ = ["attach_request_id"]
