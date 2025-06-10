from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.logging import get_logger


# 初始化日志器
logger = get_logger(__name__)

auth_scheme = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
    """
    Verify the API key provided in the Authorization header.
    """
    if not credentials or not credentials.credentials:
        logger.warning("API request attempted without credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    api_keys = [key.strip() for key in settings.API_KEYS.split(",")]
    if credentials.credentials not in api_keys:
        logger.warning(
            "API request attempted with invalid key",
            extra={
                "key_prefix": credentials.credentials[:8] + "..."
                if len(credentials.credentials) > 8
                else "***"
            },
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("API key verification successful")
