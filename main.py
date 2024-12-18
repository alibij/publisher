from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException
from pydantic import ValidationError

from v1 import v1_routers

from config.open_api import Accessibility
from config.open_api import get_routes
from common.schemas import ResponseSchema
from logger import write_log, Loggers, LogLevels
from engines.rate_limiter import limiter
from config import env_config
from error_handler import (custom_rate_limit_exceeded_handler,
                           http_error_handler,
                           validation_error_http422_error_handler,
                           aiohttp_client_error_handler)


docs_url = '/' if env_config.SWAGGER else None
redoc_url = '/redoc' if env_config.SWAGGER else None


app = FastAPI(
    default_response_class=ResponseSchema,
    docs_url=docs_url, redoc_url=redoc_url,
    title="Publisher UI",  # Set the title of the Swagger UI
    version="0.1",
)


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    get_routes(app)  # Call your route setup or initialization logic
    write_log(Loggers.APP_LOGGER, LogLevels.info,
              'fastapi startup', 'Worker started!')

    write_log.info("FastAPI app has started! Worker started!")

    yield

    write_log.info("FastAPI app is shutting down.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO add allowed hosts to .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Throttling settings
app.state.limiter = limiter


# # # Exception HYandler
# app.add_exception_handler(
#     RateLimitExceeded, custom_rate_limit_exceeded_handler)

# # # TODO add response schema for 404 error message
# app.add_exception_handler(
#     RequestValidationError, validation_error_http422_error_handler)
# app.add_exception_handler(
#     ValidationError, validation_error_http422_error_handler)

# app.add_exception_handler(
#     HTTPException, http_error_handler)
# app.add_exception_handler(
#     PyMongoError, pymongo_error_handler)

# app.add_exception_handler(
#     ClientConnectorError, aiohttp_client_error_handler)


# routes
app.include_router(v1_routers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=env_config.HOST,
        port=int(env_config.PORT),
        reload=env_config.DEBUG
    )
