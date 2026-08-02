"""
Interface (Port) for checking whether a backlink is live on a page.

The application layer depends on this abstraction, not on the concrete
HTTP client used to fetch pages. This lets us swap the implementation
(requests, httpx, a headless browser, a mock for tests) without touching
any business logic.
"""
from abc import ABC, abstractmethod

from app.domain.entities.order import LinkStatus


class LinkChecker(ABC):
    @abstractmethod
    def check(self, page_url: str, target_link: str) -> LinkStatus:
        """Fetch `page_url` and determine whether `target_link` is present."""
        ...
