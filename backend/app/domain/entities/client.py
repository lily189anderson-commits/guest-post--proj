"""
Domain Entity: Client

Pure business object. Contains NO framework, database, or web logic.
This is the heart of Clean Architecture's "Entities" layer -- it does not
know that FastAPI, SQLAlchemy, or PostgreSQL exist.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    name: str
    email: str
    phone: Optional[str] = None
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def rename(self, new_name: str) -> None:
        """Business rule: a client name cannot be blank."""
        if not new_name or not new_name.strip():
            raise ValueError("Client name cannot be empty")
        self.name = new_name.strip()
