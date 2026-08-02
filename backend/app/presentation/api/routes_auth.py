from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.auth_service import AuthService
from app.presentation.api.deps import get_auth_service
from app.presentation.schemas.auth_schema import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    token = auth_service.authenticate(payload.username, payload.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return TokenResponse(access_token=token)
