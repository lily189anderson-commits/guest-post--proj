from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClientCreateRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    notes: Optional[str] = None


class ClientUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
