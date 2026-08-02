from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderCreateRequest(BaseModel):
    client_id: int
    website_id: int
    target_link: str
    anchor_text: str
    price: float = Field(..., ge=0)


class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0)


class LinkCheckRequest(BaseModel):
    page_url: str


class BulkLinkCheckRequest(BaseModel):
    # order_id (as string key, JSON requirement) -> page_url to check against
    page_urls: dict[str, str]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    website_id: int
    target_link: str
    anchor_text: str
    price: float
    paid_amount: float
    pending_amount: float
    payment_status: str
    link_status: str
    last_checked_at: Optional[datetime] = None
    created_at: datetime
