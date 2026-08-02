"""
Domain Entity: Website

Represents a blog/site that hosts guest posts, along with its
quality metrics (DA/DR - Domain Authority / Domain Rating).
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Website:
    domain: str
    da_score: int = 0
    dr_score: int = 0
    niche: Optional[str] = None
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def update_metrics(self, da_score: int, dr_score: int) -> None:
        """Business rule: DA/DR scores must be within 0-100."""
        if not (0 <= da_score <= 100) or not (0 <= dr_score <= 100):
            raise ValueError("DA/DR scores must be between 0 and 100")
        self.da_score = da_score
        self.dr_score = dr_score
