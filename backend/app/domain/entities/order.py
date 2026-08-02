"""
Domain Entity: Order (a guest-post / backlink placement)

Encapsulates the core business rules around an order's lifecycle:
- link health (Active / Broken / Pending)
- payment state (earnings & pending payments are derived from this)
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class LinkStatus(str, Enum):
    PENDING = "pending"      # not yet checked
    ACTIVE = "active"        # link found on the page
    BROKEN = "broken"        # link missing / page unreachable


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"


@dataclass
class Order:
    client_id: int
    website_id: int
    target_link: str
    anchor_text: str
    price: float
    id: Optional[int] = None
    paid_amount: float = 0.0
    payment_status: PaymentStatus = PaymentStatus.UNPAID
    link_status: LinkStatus = LinkStatus.PENDING
    last_checked_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def pending_amount(self) -> float:
        return round(self.price - self.paid_amount, 2)

    def record_payment(self, amount: float) -> None:
        """Business rule: cannot overpay; auto-derives payment_status."""
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        if self.paid_amount + amount > self.price + 1e-9:
            raise ValueError("Payment exceeds order price")
        self.paid_amount = round(self.paid_amount + amount, 2)
        if self.paid_amount >= self.price:
            self.payment_status = PaymentStatus.PAID
        elif self.paid_amount > 0:
            self.payment_status = PaymentStatus.PARTIAL
        else:
            self.payment_status = PaymentStatus.UNPAID

    def mark_checked(self, link_status: LinkStatus, checked_at: datetime) -> None:
        self.link_status = link_status
        self.last_checked_at = checked_at
