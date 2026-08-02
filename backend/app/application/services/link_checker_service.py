"""
Application Service: LinkCheckerService

Implements the "Automated Link Health Checker" feature. It depends on the
abstract LinkChecker interface (not on `requests`/`httpx` directly), and
on the OrderRepository -- both injected. Swapping the HTTP mechanism or
the storage mechanism never requires touching this class.
"""
from datetime import datetime
from typing import Optional

from app.application.interfaces.link_checker_interface import LinkChecker
from app.domain.entities.order import Order, LinkStatus
from app.domain.repositories.interfaces import OrderRepository, WebsiteRepository


class LinkCheckerService:
    def __init__(self, order_repository: OrderRepository,
                 website_repository: WebsiteRepository,
                 link_checker: LinkChecker):
        self._orders = order_repository
        self._websites = website_repository
        self._checker = link_checker

    def check_order(self, order_id: int, page_url: str) -> Order:
        """Check a single order's backlink against the given page URL."""
        order = self._orders.get_by_id(order_id)
        if order is None:
            raise LookupError(f"Order {order_id} not found")

        status = self._checker.check(page_url=page_url, target_link=order.target_link)
        order.mark_checked(status, datetime.utcnow())
        return self._orders.update(order)

    def check_all(self, page_urls: dict) -> list:
        """
        Bulk-check every order. `page_urls` maps order_id -> the guest-post
        page URL that should contain the backlink.
        """
        results = []
        for order in self._orders.list_all():
            page_url = page_urls.get(order.id)
            if not page_url:
                continue
            status = self._checker.check(page_url=page_url, target_link=order.target_link)
            order.mark_checked(status, datetime.utcnow())
            results.append(self._orders.update(order))
        return results
