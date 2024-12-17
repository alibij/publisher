import json
from datetime import timedelta
from fastapi import Depends, Request
from passlib.context import CryptContext

from common.schemas import TokenData
from common.utiles import tehrantimenow
from common.exceptions import AuthenticationError
from config import env_config
from jose import jwt, JWTError

# password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    """Check the password with its hash"""
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    """Hashes the password"""
    return pwd_context.hash(password)


# token
async def get_token_expire_time(minutes: int = None):
    min = minutes if minutes else env_config.ACCESS_TOKEN_EXPIRE_MINUTES
    return int(tehrantimenow().timestamp() + min*60)


async def create_access_token(data: dict, request: Request = None):
    """Create an access token using jwt lib"""
    user_agent = request.headers.get(
        "user-agent", "unknown") if request else None

    to_encode = {
        "data": data.dict(),
        "user_agent": user_agent,
        "token_exp": await get_token_expire_time()
    }

    encoded_jwt = jwt.encode(
        to_encode, env_config.SECRET_KEY,
        algorithm=env_config.ALGORITHM)
    return encoded_jwt


async def get_token_data(token: str, request: Request) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            env_config.SECRET_KEY,
            algorithms=[env_config.ALGORITHM]
        )

        payload = TokenData(**payload)
        if not payload.data:
            raise AuthenticationError()

        if payload.token_exp <= tehrantimenow().timestamp():
            raise AuthenticationError()

        request_user_agent = request.headers.get("user-agent", "unknown")

        if payload.user_agent != request_user_agent:
            raise AuthenticationError()

        return payload.data

    except JWTError:
        raise AuthenticationError()
