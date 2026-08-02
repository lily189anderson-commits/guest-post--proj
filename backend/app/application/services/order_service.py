"""
Application Service: OrderService

Handles the "Client & Order Management" feature -- creating orders that
tie a client, a target website, a backlink URL, anchor text, and a price
together -- plus recording payments (feeds the analytics feature).
"""
from typing import List, Optional

from app.domain.entities.order import Order
from app.domain.repositories.interfaces import OrderRepository, ClientRepository, WebsiteRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository,
                 client_repository: ClientRepository,
                 website_repository: WebsiteRepository):
        self._orders = order_repository
        self._clients = client_repository
        self._websites = website_repository

    def create_order(self, client_id: int, website_id: int, target_link: str,
                      anchor_text: str, price: float) -> Order:
        if self._clients.get_by_id(client_id) is None:
            raise LookupError(f"Client {client_id} not found")
        if self._websites.get_by_id(website_id) is None:
            raise LookupError(f"Website {website_id} not found")
        if price < 0:
            raise ValueError("Price cannot be negative")
        order = Order(client_id=client_id, website_id=website_id,
                       target_link=target_link.strip(), anchor_text=anchor_text.strip(),
                       price=price)
        return self._orders.create(order)

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._orders.get_by_id(order_id)

    def list_orders(self) -> List[Order]:
        return self._orders.list_all()

    def record_payment(self, order_id: int, amount: float) -> Order:
        order = self._orders.get_by_id(order_id)
        if order is None:
            raise LookupError(f"Order {order_id} not found")
        order.record_payment(amount)
        return self._orders.update(order)

    def delete_order(self, order_id: int) -> bool:
        return self._orders.delete(order_id)
