import logging
import os
import jwt
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import httpx

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
USER_AGENT = "osm-wikidata-matcher-neo 1.0 (https://github.com/anomalyco/opencode)"

ACCESS_TOKEN = os.getenv("WIKIMEDIA_ACCESS_TOKEN", "")
CONSUMER_KEY = os.getenv("WIKIMEDIA_CLIENT_KEY", "")
WIKIDATA_USERNAME = os.getenv("WIKIDATA_USERNAME", "")


class AuthStatus(BaseModel):
    logged_in: bool
    username: str | None = None


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except Exception:
        return None


@router.get("/status", response_model=AuthStatus)
async def auth_status():
    if not ACCESS_TOKEN:
        return AuthStatus(logged_in=False)

    token_data = decode_token(ACCESS_TOKEN)
    if not token_data:
        return AuthStatus(logged_in=False)

    username = None
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            WIKIDATA_API_URL,
            params={"action": "query", "meta": "userinfo", "format": "json"},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            username = data.get("query", {}).get("userinfo", {}).get("name")

    if not username and token_data.get("sub"):
        username = f"User:{token_data['sub']}"

    return AuthStatus(logged_in=True, username=username)


@router.get("/login")
async def login():
    if not CONSUMER_KEY:
        raise HTTPException(status_code=503, detail="OAuth not configured - set WIKIMEDIA_CLIENT_KEY in .env")
    raise HTTPException(status_code=501, detail="OAuth login flow not yet implemented")


@router.get("/callback")
async def callback(request: Request):
    raise HTTPException(status_code=501, detail="OAuth callback not yet implemented")


@router.post("/logout")
async def logout():
    return {"status": "ok"}
