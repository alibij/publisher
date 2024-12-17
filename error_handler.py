from typing import Union

from bson.errors import InvalidId
from fastapi import HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, ORJSONResponse
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from slowapi.errors import RateLimitExceeded
from aiohttp.client_exceptions import ClientConnectorError

from common.exceptions import ServerError, NotAcceptableError


async def validation_error_http422_error_handler(
        _: Request,
        exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    errors = exc.errors()
    errors[0].update({"code": 'Value is not valid'})

    return ORJSONResponse(
        {"status": "fail", "errors": errors},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_error_handler(_: Request, exc: HTTPException) -> ORJSONResponse:
    return ORJSONResponse({"status": "fail", "errors": [{'msg': exc.detail}]}, status_code=exc.status_code)


def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Build a simple JSON response that includes the details of the rate limit
    that was hit. If no limit is hit, the countdown is added to headers.
    """
    detail = exc.detail  # can be used for later(info about limit counts)
    response = ORJSONResponse(
        {"status": "fail", "errors": [{'msg': "Rate limit exceeded"}]}, status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response


async def pymongo_error_handler(_: Request, exc: PyMongoError):
    return await http_error_handler(_,
                                    ServerError(
                                        'Database problem occurred.'))


async def objectid_error_handler(_: Request, exc: InvalidId):
    return await http_error_handler(_,
                                    NotAcceptableError(
                                        "ObjectID in Not Valid"))


async def aiohttp_client_error_handler(_: Request,
                                       exc: ClientConnectorError):
    return await http_error_handler(_, ServerError())
