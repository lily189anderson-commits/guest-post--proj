"""
Application Service: AuthService

Handles login: verifying credentials and issuing a JWT. Password hashing
and JWT encoding are infrastructure concerns, injected here as callables/
objects so this service stays framework-agnostic and testable.
"""
from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.interfaces import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, password_hasher, token_issuer):
        """
        password_hasher: object with .hash(plain) and .verify(plain, hashed)
        token_issuer: object with .issue(subject: str) -> str
        """
        self._users = user_repository
        self._hasher = password_hasher
        self._tokens = token_issuer

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Returns a JWT access token if credentials are valid, else None."""
        user = self._users.get_by_username(username)
        if user is None:
            return None
        if not self._hasher.verify(password, user.hashed_password):
            return None
        return self._tokens.issue(subject=user.username)

    def register(self, username: str, password: str, full_name: Optional[str] = None) -> User:
        if self._users.get_by_username(username) is not None:
            raise ValueError("Username already exists")
        user = User(username=username, hashed_password=self._hasher.hash(password), full_name=full_name)
        return self._users.create(user)
