from fastapi import HTTPException, status

from common.resources import response_data


__all__ = ['AuthenticationError', 'NotFoundError',
           'ForbiddenError', 'NotAcceptableError', 'DuplicateError']


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = response_data.UNAUTHORIZED):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        # self.headers = {"WWW-Authenticate": "Bearer"}


class NotFoundError(HTTPException):
    def __init__(self, detail: str = response_data.NOT_FOUND):
        self.detail = detail
        self.status_code = status.HTTP_404_NOT_FOUND


class ForbiddenError(HTTPException):

    def __init__(self, detail: str):
        self.detail = detail
        self.status_code = status.HTTP_403_FORBIDDEN


class NotAcceptableError(HTTPException):
    def __init__(self, detail: str):

        self.detail = detail
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE


class DuplicateError(HTTPException):
    def __init__(self, detail: str = response_data.DUPLICATE_ERROR) -> None:
        self.detail = detail
        self.status_code = status.HTTP_409_CONFLICT


class SMSServerError(HTTPException):
    def __init__(self, detail: str = 'sms server problems.'):
        self.detail = detail
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ServerError(HTTPException):
    def __init__(self, detail: str = 'server problems.'):
        self.detail = detail
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class PaymentError(HTTPException):
    def __init__(self, Code: str = status.HTTP_406_NOT_ACCEPTABLE, detail: str = 'payment problems.'):
        self.detail = detail
        self.status_code = Code
