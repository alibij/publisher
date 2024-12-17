from fastapi import Depends
from common.exceptions import AuthenticationError
from common.jwt_bearer import JWTBearer
from models.mongo.admin import AdminUserModel


oauth2_scheme = JWTBearer()


async def get_token_user(user: AdminUserModel = Depends(oauth2_scheme)):
    user = AdminUserModel.parse_obj(user)
    if user:
        return user
    raise AuthenticationError("Failed to get User")
