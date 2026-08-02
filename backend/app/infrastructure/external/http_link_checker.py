"""
Concrete adapter implementing the LinkChecker port using real HTTP requests.

Fetches the guest-post page and checks whether the client's target link
appears anywhere in the page's HTML (as an href or plain text occurrence).
"""
import requests

from app.application.interfaces.link_checker_interface import LinkChecker
from app.domain.entities.order import LinkStatus


class HttpLinkChecker(LinkChecker):
    def __init__(self, timeout: int = 10):
        self._timeout = timeout

    def check(self, page_url: str, target_link: str) -> LinkStatus:
        try:
            response = requests.get(
                page_url,
                timeout=self._timeout,
                headers={"User-Agent": "GuestPostBacklinkEngine/1.0 (+link-health-checker)"},
            )
            if response.status_code >= 400:
                return LinkStatus.BROKEN

            html = response.text
            normalized_target = target_link.strip().lower()
            if normalized_target in html.lower():
                return LinkStatus.ACTIVE
            return LinkStatus.BROKEN
        except requests.RequestException:
            return LinkStatus.BROKEN
