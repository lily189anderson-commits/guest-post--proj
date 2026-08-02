"""
Application Service: WebsiteService

Handles the "Website Metrics Logger" feature: recording which sites
guest posts are placed on, along with DA/DR quality scores.
"""
from typing import List, Optional

from app.domain.entities.website import Website
from app.domain.repositories.interfaces import WebsiteRepository


class WebsiteService:
    def __init__(self, website_repository: WebsiteRepository):
        self._repo = website_repository

    def create_website(self, domain: str, da_score: int, dr_score: int,
                        niche: Optional[str], notes: Optional[str]) -> Website:
        website = Website(domain=domain.strip().lower(), da_score=da_score,
                           dr_score=dr_score, niche=niche, notes=notes)
        if not website.domain:
            raise ValueError("Website domain is required")
        return self._repo.create(website)

    def get_website(self, website_id: int) -> Optional[Website]:
        return self._repo.get_by_id(website_id)

    def list_websites(self) -> List[Website]:
        return self._repo.list_all()

    def update_metrics(self, website_id: int, da_score: int, dr_score: int) -> Website:
        website = self._repo.get_by_id(website_id)
        if website is None:
            raise LookupError(f"Website {website_id} not found")
        website.update_metrics(da_score, dr_score)
        return self._repo.update(website)

    def delete_website(self, website_id: int) -> bool:
        return self._repo.delete(website_id)
