"""
Composition Root / Dependency Injection wiring.

This is the ONLY place where concrete infrastructure classes (SQLAlchemy
repositories, the HTTP link checker, security adapters) are wired together
into the abstract interfaces that services depend on. FastAPI's `Depends`
mechanism performs the injection per-request.

If you swap PostgreSQL for MongoDB, or `requests` for `httpx`, this file
(plus the concrete adapter) is all that changes -- domain and application
layers stay untouched.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import password_hasher, token_issuer
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_client_repository import SqlAlchemyClientRepository
from app.infrastructure.repositories.sqlalchemy_website_repository import SqlAlchemyWebsiteRepository
from app.infrastructure.repositories.sqlalchemy_order_repository import SqlAlchemyOrderRepository
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.infrastructure.external.http_link_checker import HttpLinkChecker

from app.application.services.client_service import ClientService
from app.application.services.website_service import WebsiteService
from app.application.services.order_service import OrderService
from app.application.services.link_checker_service import LinkCheckerService
from app.application.services.analytics_service import AnalyticsService
from app.application.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- Repositories -----------------------------------------------------------

def get_client_repository(db: Session = Depends(get_db)) -> SqlAlchemyClientRepository:
    return SqlAlchemyClientRepository(db)


def get_website_repository(db: Session = Depends(get_db)) -> SqlAlchemyWebsiteRepository:
    return SqlAlchemyWebsiteRepository(db)


def get_order_repository(db: Session = Depends(get_db)) -> SqlAlchemyOrderRepository:
    return SqlAlchemyOrderRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db)


# --- Services ----------------------------------------------------------------

def get_client_service(repo: SqlAlchemyClientRepository = Depends(get_client_repository)) -> ClientService:
    return ClientService(repo)


def get_website_service(repo: SqlAlchemyWebsiteRepository = Depends(get_website_repository)) -> WebsiteService:
    return WebsiteService(repo)


def get_order_service(
    order_repo: SqlAlchemyOrderRepository = Depends(get_order_repository),
    client_repo: SqlAlchemyClientRepository = Depends(get_client_repository),
    website_repo: SqlAlchemyWebsiteRepository = Depends(get_website_repository),
) -> OrderService:
    return OrderService(order_repo, client_repo, website_repo)


def get_link_checker_service(
    order_repo: SqlAlchemyOrderRepository = Depends(get_order_repository),
    website_repo: SqlAlchemyWebsiteRepository = Depends(get_website_repository),
) -> LinkCheckerService:
    return LinkCheckerService(order_repo, website_repo, HttpLinkChecker())


def get_analytics_service(
    order_repo: SqlAlchemyOrderRepository = Depends(get_order_repository),
    client_repo: SqlAlchemyClientRepository = Depends(get_client_repository),
) -> AnalyticsService:
    return AnalyticsService(order_repo, client_repo)


def get_auth_service(user_repo: SqlAlchemyUserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo, password_hasher, token_issuer)


# --- Auth guard ----------------------------------------------------------------

def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    username = token_issuer.decode(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
