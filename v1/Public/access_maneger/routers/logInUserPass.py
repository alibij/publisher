from fastapi import APIRouter, Depends, Form, Request
from passlib.context import CryptContext
from engines.rate_limiter import limiter


from common.exceptions import AuthenticationError
from common.headers import db_header
from common.token import create_access_token, verify_password
from db.mongo.crud import MongoCrud
from db.mongo.engine import Mongo
from models.mongo.admin import AdminUserModel
from ..schemas import TokenOut, UserDataInToken


router = APIRouter(prefix='')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
@ limiter.limit('1/second,5/minutes')
async def get_access_token(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Mongo = Depends(db_header)
):

    user = await MongoCrud(db, AdminUserModel).find_one(
        {AdminUserModel.username: username}
    )

    if not user or not await verify_password(password, user.hash_password):
        raise AuthenticationError()

    access_token = await create_access_token(
        UserDataInToken.parse_obj(user),
        request=request
    )

    return TokenOut(
        token=access_token,
        type="bearer"
    )
