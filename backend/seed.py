"""
Run once after setting up the database:

    python seed.py

Creates the tables (if not present) and a default admin user so you can
log in immediately. Credentials come from .env (DEFAULT_ADMIN_USERNAME /
DEFAULT_ADMIN_PASSWORD) -- change them there before running in production.
"""
from app.core.config import settings
from app.core.security import password_hasher, token_issuer
from app.infrastructure.database.session import init_db, SessionLocal
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.application.services.auth_service import AuthService


def main():
    init_db()
    db = SessionLocal()
    try:
        user_repo = SqlAlchemyUserRepository(db)
        auth_service = AuthService(user_repo, password_hasher, token_issuer)

        existing = user_repo.get_by_username(settings.DEFAULT_ADMIN_USERNAME)
        if existing:
            print(f"Admin user '{settings.DEFAULT_ADMIN_USERNAME}' already exists. Skipping.")
            return

        auth_service.register(
            username=settings.DEFAULT_ADMIN_USERNAME,
            password=settings.DEFAULT_ADMIN_PASSWORD,
            full_name="Administrator",
        )
        print(f"Created admin user: {settings.DEFAULT_ADMIN_USERNAME} / {settings.DEFAULT_ADMIN_PASSWORD}")
        print("IMPORTANT: change this password (or the .env defaults) before real use.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
