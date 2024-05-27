from fastapi import Header, HTTPException
from app.config import get_settings

settings = get_settings()


def api_key_auth(api_key: str = Header(...)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
