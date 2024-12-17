from typing import Any

from fastapi.responses import ORJSONResponse
from pydantic import BaseModel


class ResponseSchema(ORJSONResponse):
    def __init__(self,
                 content: Any = [],
                 status_code: int = 200,
                 headers: dict = None,
                 media_type: str = None,
                 background=None,
                 status: str = 'ok',
                 errors: dict = []):

        out_put = {
            'status': status,
            'data': content,
            'errors': errors
        }

        super().__init__(out_put, status_code, headers, media_type, background)


class UniqueResponse:
    def __init__(self, msg=None, **kwargs):
        if msg:
            self.msg = msg

        # set attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dict(self):
        return self.__dict__


class TokenData(BaseModel):
    data: dict = None
    token_exp: int = None
    token: str = None
    user_agent: str = None
