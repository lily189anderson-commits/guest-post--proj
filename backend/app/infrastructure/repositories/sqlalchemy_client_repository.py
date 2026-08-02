from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.client import Client
from app.domain.repositories.interfaces import ClientRepository
from app.infrastructure.database.models import ClientModel


def _to_entity(row: ClientModel) -> Client:
    return Client(
        id=row.id, name=row.name, email=row.email, phone=row.phone,
        notes=row.notes, created_at=row.created_at,
    )


class SqlAlchemyClientRepository(ClientRepository):
    """Concrete adapter implementing the ClientRepository port using SQLAlchemy."""

    def __init__(self, db: Session):
        self._db = db

    def create(self, client: Client) -> Client:
        row = ClientModel(name=client.name, email=client.email, phone=client.phone, notes=client.notes)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def get_by_id(self, client_id: int) -> Optional[Client]:
        row = self._db.query(ClientModel).filter(ClientModel.id == client_id).first()
        return _to_entity(row) if row else None

    def list_all(self) -> List[Client]:
        return [_to_entity(r) for r in self._db.query(ClientModel).order_by(ClientModel.id.desc()).all()]

    def update(self, client: Client) -> Client:
        row = self._db.query(ClientModel).filter(ClientModel.id == client.id).first()
        if row is None:
            raise LookupError(f"Client {client.id} not found")
        row.name = client.name
        row.email = client.email
        row.phone = client.phone
        row.notes = client.notes
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def delete(self, client_id: int) -> bool:
        row = self._db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
