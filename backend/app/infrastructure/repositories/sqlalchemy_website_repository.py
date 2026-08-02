from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.website import Website
from app.domain.repositories.interfaces import WebsiteRepository
from app.infrastructure.database.models import WebsiteModel


def _to_entity(row: WebsiteModel) -> Website:
    return Website(
        id=row.id, domain=row.domain, da_score=row.da_score, dr_score=row.dr_score,
        niche=row.niche, notes=row.notes, created_at=row.created_at,
    )


class SqlAlchemyWebsiteRepository(WebsiteRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(self, website: Website) -> Website:
        row = WebsiteModel(domain=website.domain, da_score=website.da_score,
                            dr_score=website.dr_score, niche=website.niche, notes=website.notes)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def get_by_id(self, website_id: int) -> Optional[Website]:
        row = self._db.query(WebsiteModel).filter(WebsiteModel.id == website_id).first()
        return _to_entity(row) if row else None

    def list_all(self) -> List[Website]:
        return [_to_entity(r) for r in self._db.query(WebsiteModel).order_by(WebsiteModel.id.desc()).all()]

    def update(self, website: Website) -> Website:
        row = self._db.query(WebsiteModel).filter(WebsiteModel.id == website.id).first()
        if row is None:
            raise LookupError(f"Website {website.id} not found")
        row.domain = website.domain
        row.da_score = website.da_score
        row.dr_score = website.dr_score
        row.niche = website.niche
        row.notes = website.notes
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def delete(self, website_id: int) -> bool:
        row = self._db.query(WebsiteModel).filter(WebsiteModel.id == website_id).first()
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
