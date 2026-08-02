"""
Application Service: ClientService

Orchestrates use-cases around clients. Depends only on the abstract
ClientRepository (injected), never on a concrete database implementation.
This is Dependency Injection + the Repository/Service pattern together.
"""
from typing import List, Optional

from app.domain.entities.client import Client
from app.domain.repositories.interfaces import ClientRepository


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self._repo = client_repository

    def create_client(self, name: str, email: str, phone: Optional[str], notes: Optional[str]) -> Client:
        client = Client(name=name.strip(), email=email.strip().lower(), phone=phone, notes=notes)
        if not client.name:
            raise ValueError("Client name is required")
        return self._repo.create(client)

    def get_client(self, client_id: int) -> Optional[Client]:
        return self._repo.get_by_id(client_id)

    def list_clients(self) -> List[Client]:
        return self._repo.list_all()

    def update_client(self, client_id: int, name: Optional[str], email: Optional[str],
                       phone: Optional[str], notes: Optional[str]) -> Client:
        client = self._repo.get_by_id(client_id)
        if client is None:
            raise LookupError(f"Client {client_id} not found")
        if name:
            client.rename(name)
        if email:
            client.email = email.strip().lower()
        if phone is not None:
            client.phone = phone
        if notes is not None:
            client.notes = notes
        return self._repo.update(client)

    def delete_client(self, client_id: int) -> bool:
        return self._repo.delete(client_id)
