from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from .token import get_token_data
from .schemas import TokenData


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(
            auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenData:
        # credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        authorization = request.headers.get("Authorization")
        # print(authorization)
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=401, detail="Not authenticated"
                )
            else:
                return None

        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials",
                )
            else:
                return None

        return await get_token_data(credentials, request)
