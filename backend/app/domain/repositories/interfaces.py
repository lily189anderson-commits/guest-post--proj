"""
Repository Interfaces (Ports)

These are ABSTRACT contracts. The domain/application layers depend only on
these interfaces, never on concrete database code. This is the Dependency
Inversion Principle (the "D" in SOLID) in action: high-level modules
(services) do not depend on low-level modules (SQLAlchemy repositories);
both depend on this abstraction.

Concrete implementations live in infrastructure/repositories/*.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.client import Client
from app.domain.entities.order import Order
from app.domain.entities.website import Website
from app.domain.entities.user import User


class ClientRepository(ABC):
    @abstractmethod
    def create(self, client: Client) -> Client: ...

    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[Client]: ...

    @abstractmethod
    def list_all(self) -> List[Client]: ...

    @abstractmethod
    def update(self, client: Client) -> Client: ...

    @abstractmethod
    def delete(self, client_id: int) -> bool: ...


class WebsiteRepository(ABC):
    @abstractmethod
    def create(self, website: Website) -> Website: ...

    @abstractmethod
    def get_by_id(self, website_id: int) -> Optional[Website]: ...

    @abstractmethod
    def list_all(self) -> List[Website]: ...

    @abstractmethod
    def update(self, website: Website) -> Website: ...

    @abstractmethod
    def delete(self, website_id: int) -> bool: ...


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> Order: ...

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]: ...

    @abstractmethod
    def list_all(self) -> List[Order]: ...

    @abstractmethod
    def update(self, order: Order) -> Order: ...

    @abstractmethod
    def delete(self, order_id: int) -> bool: ...


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    def create(self, user: User) -> User: ...
