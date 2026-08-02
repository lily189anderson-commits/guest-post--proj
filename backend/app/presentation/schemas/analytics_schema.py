from typing import List

from pydantic import BaseModel


class ClientRevenueResponse(BaseModel):
    client_id: int
    client_name: str
    total_orders: int
    total_earned: float
    total_pending: float


class AnalyticsSummaryResponse(BaseModel):
    total_revenue_collected: float
    total_revenue_expected: float
    total_pending: float
    total_orders: int
    per_client: List[ClientRevenueResponse]
