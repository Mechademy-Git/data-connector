from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import settings


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ):
        if credentials:
            token = credentials.credentials
            if token == settings.api_key:
                return token
            raise HTTPException(
                status_code=403, detail="Invalid token or token expired"
            )
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
