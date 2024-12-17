from fastapi import APIRouter, Depends


from common.exceptions import NotAcceptableError, NotFoundError
from common.headers import db_header
from common.resources import response_data
from common.schemas import UniqueResponse
from common.token import get_password_hash, verify_password
from common.utiles import get_unique_code
from db.mongo.crud import MongoCrud
from db.mongo.engine import Mongo
from models.mongo.admin import AdminUserModel, AdminUserUTypesME
from v1.Panel.access_maneger.dependencies import get_token_user
from ..schemas import AdminGetOut, ChangPassAdminPostIn, SingUpAdminPostIn, SingUpAdminPutIn


router = APIRouter(prefix='/admin')


@router.post("")
async def new_admin_post(
    data: SingUpAdminPostIn,
    db: Mongo = Depends(db_header)
):
    if data.utype == AdminUserUTypesME.super_user:
        raise NotAcceptableError("You can't Add SuperUser")

    data.username = data.username.lower()
    user = await MongoCrud(db, AdminUserModel).find_one(
        {AdminUserModel.username: data.username}
    )
    if user:
        raise NotAcceptableError("Username Already Taken")

    await MongoCrud(db, AdminUserModel).insert_one(
        AdminUserModel(
            **data.dict(),
            code=get_unique_code(),
            hash_password=await get_password_hash(data.password))
    )

    return UniqueResponse(response_data.CREATED)


@router.put("")
async def edit_admin_put(
    data: SingUpAdminPutIn,
    db: Mongo = Depends(db_header)
):
    if data.username:
        data.username = data.username.lower()

    user = await MongoCrud(db, AdminUserModel).find_one(
        {AdminUserModel.code: data.code}
    )

    if not user:
        raise NotFoundError("Admin Not Find")

    if user.utype == AdminUserUTypesME.super_user:
        raise NotAcceptableError("You can't Edit SuperUser")

    item = AdminUserModel(
        **data.dict(),
        **({"hash_password": await get_password_hash(data.password)} if data.password else {})
    )
    await MongoCrud(db, AdminUserModel).update_one_set(
        {AdminUserModel.code: data.code},
        item
    )

    return UniqueResponse(response_data.UPDATED)


@router.delete("")
async def delete_admin(
    code: str,
    db: Mongo = Depends(db_header)
):
    user = await MongoCrud(db, AdminUserModel).find_one({AdminUserModel.code: code})

    if user and user.utype == AdminUserUTypesME.super_user:
        raise NotAcceptableError("You can't Delete SuperUser")

    await MongoCrud(db, AdminUserModel).delete(
        {AdminUserModel.code: code}
    )

    return UniqueResponse(response_data.DELETED)


@router.get("")
async def get_all_admin(
    admin_code: str = None,
    db: Mongo = Depends(db_header)
):
    query = {AdminUserModel.utype: {"$ne": AdminUserUTypesME.super_user}}
    if admin_code:
        query.update({AdminUserModel.code: admin_code})

    d = await MongoCrud(db, AdminUserModel).find(
        query
    )
    d = AdminGetOut(data=d)
    return d.data


@router.post("/chang_password")
async def change_password_admin_post(
    data: ChangPassAdminPostIn,
    user=Depends(get_token_user),
    db: Mongo = Depends(db_header)
):

    if user := await MongoCrud(db, AdminUserModel).find_one(
        {AdminUserModel.code: user.code}
    ):

        if user.utype == AdminUserUTypesME.super_user:
            raise NotAcceptableError("You can't Change SuperUser Password")

        if not await verify_password(data.old_password, user.hash_password):
            raise NotAcceptableError("Incorrect Old Password")

        await MongoCrud(db, AdminUserModel).update_one_set(
            {AdminUserModel.code: user.code},
            {AdminUserModel.hash_password: await get_password_hash(data.new_password)}
        )
        return UniqueResponse(response_data.UPDATED)

    raise NotAcceptableError("User Not Found")
