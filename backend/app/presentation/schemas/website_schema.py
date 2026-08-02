from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WebsiteCreateRequest(BaseModel):
    domain: str
    da_score: int = Field(0, ge=0, le=100)
    dr_score: int = Field(0, ge=0, le=100)
    niche: Optional[str] = None
    notes: Optional[str] = None


class WebsiteMetricsUpdateRequest(BaseModel):
    da_score: int = Field(..., ge=0, le=100)
    dr_score: int = Field(..., ge=0, le=100)


class WebsiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    da_score: int
    dr_score: int
    niche: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
