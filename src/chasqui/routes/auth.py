import logging
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from chasqui.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

_admin_scheme = HTTPBearer()


async def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(_admin_scheme),
) -> None:
    """Validate the admin secret (Bearer token)."""
    if credentials.credentials != settings.admin_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin secret",
        )


class TokenRequest(BaseModel):
    client_id: str = Field(min_length=1, description="Client identifier (becomes the 'sub' claim)")
    expires_in_days: int = Field(default=90, gt=0, le=365, description="Token validity in days")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    client_id: str
    expires_at: str


@router.post("/token", dependencies=[Depends(require_admin)], response_model=TokenResponse)
async def create_token(req: TokenRequest) -> TokenResponse:
    """Issue a JWT for an API client. Requires admin secret."""
    now = datetime.now(UTC)
    exp = now + timedelta(days=req.expires_in_days)
    payload = {"sub": req.client_id, "iat": now, "exp": exp}

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    logger.info("Issued token for client %r, expires %s", req.client_id, exp.isoformat())
    return TokenResponse(
        access_token=token,
        client_id=req.client_id,
        expires_at=exp.isoformat(),
    )
