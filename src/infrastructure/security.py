import os
from fastapi import Header, HTTPException, status

API_TOKEN = os.getenv("WHISPER_SHIELD_API_TOKEN", "whisper-shield-dev-token-2026")

async def validate_api_token(x_api_token: str = Header(None)):
    """Simple API token validation middleware."""
    if not x_api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Token missing"
        )
    
    if x_api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Token"
        )
    return x_api_token
