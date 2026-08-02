"""
Application Service: AnalyticsService

Implements the "Revenue & Earnings Analytics" feature: total earnings,
pending payments, and a per-client revenue breakdown -- all derived from
Order data, with no duplicate storage of "totals" anywhere (single source
of truth = the orders table).
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from app.domain.repositories.interfaces import OrderRepository, ClientRepository


@dataclass
class ClientRevenue:
    client_id: int
    client_name: str
    total_orders: int
    total_earned: float
    total_pending: float


@dataclass
class AnalyticsSummary:
    total_revenue_collected: float
    total_revenue_expected: float
    total_pending: float
    total_orders: int
    per_client: List[ClientRevenue]


class AnalyticsService:
    def __init__(self, order_repository: OrderRepository, client_repository: ClientRepository):
        self._orders = order_repository
        self._clients = client_repository

    def summary(self) -> AnalyticsSummary:
        orders = self._orders.list_all()
        clients = {c.id: c for c in self._clients.list_all()}

        per_client_totals: Dict[int, Dict[str, float]] = defaultdict(
            lambda: {"count": 0, "earned": 0.0, "pending": 0.0}
        )

        total_collected = 0.0
        total_expected = 0.0

        for order in orders:
            total_collected += order.paid_amount
            total_expected += order.price
            bucket = per_client_totals[order.client_id]
            bucket["count"] += 1
            bucket["earned"] += order.paid_amount
            bucket["pending"] += order.pending_amount

        per_client = [
            ClientRevenue(
                client_id=cid,
                client_name=clients[cid].name if cid in clients else "Unknown",
                total_orders=int(data["count"]),
                total_earned=round(data["earned"], 2),
                total_pending=round(data["pending"], 2),
            )
            for cid, data in per_client_totals.items()
        ]
        per_client.sort(key=lambda x: x.total_earned, reverse=True)

        return AnalyticsSummary(
            total_revenue_collected=round(total_collected, 2),
            total_revenue_expected=round(total_expected, 2),
            total_pending=round(total_expected - total_collected, 2),
            total_orders=len(orders),
            per_client=per_client,
        )
