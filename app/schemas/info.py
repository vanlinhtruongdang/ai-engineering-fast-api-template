from pydantic import BaseModel


class SystemInfoResponse(BaseModel):
    status: str
    name: str
    version: str
    environment: str
