"""
Security adapters: password hashing (bcrypt via passlib) and JWT issuance/
verification (python-jose). These are the concrete objects injected into
AuthService as `password_hasher` and `token_issuer` -- AuthService itself
never imports bcrypt or jose directly.
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    def hash(self, plain_password: str) -> str:
        return _pwd_context.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)


class TokenIssuer:
    def issue(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode(self, token: str) -> Optional[str]:
        """Returns the username (subject) if the token is valid, else None."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None


password_hasher = PasswordHasher()
token_issuer = TokenIssuer()
