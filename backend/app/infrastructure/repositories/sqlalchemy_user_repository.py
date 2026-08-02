from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.interfaces import UserRepository
from app.infrastructure.database.models import UserModel


def _to_entity(row: UserModel) -> User:
    return User(id=row.id, username=row.username, hashed_password=row.hashed_password,
                full_name=row.full_name, created_at=row.created_at)


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_by_username(self, username: str) -> Optional[User]:
        row = self._db.query(UserModel).filter(UserModel.username == username).first()
        return _to_entity(row) if row else None

    def create(self, user: User) -> User:
        row = UserModel(username=user.username, hashed_password=user.hashed_password,
                         full_name=user.full_name)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)
