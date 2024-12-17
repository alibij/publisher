from pydantic import BaseModel


class TokenOut(BaseModel):
    token: str
    type: str


class UserDataInToken(BaseModel):
    code: str
    username: str
    utype: str
