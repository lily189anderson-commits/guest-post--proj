"""
Domain Entity: User

Represents an authenticated operator of the system (agency owner / staff).
Password hashing is an infrastructure concern -- this entity only stores
the resulting hash, never plain-text passwords.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    username: str
    hashed_password: str
    id: Optional[int] = None
    full_name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
