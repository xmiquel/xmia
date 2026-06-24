from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from mt5.errors import (
    AdapterNotConnectedError,
    AuthenticationError,
    ConnectionError,
    TerminalNotAvailableError,
)


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AdapterNotConnectedError)
    async def adapter_not_connected(request: Request, exc: AdapterNotConnectedError):
        return JSONResponse(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TerminalNotAvailableError)
    async def terminal_not_available(request: Request, exc: TerminalNotAvailableError):
        return JSONResponse(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConnectionError)
    async def connection_error(request: Request, exc: ConnectionError):
        return JSONResponse(
            status_code=HTTP_502_BAD_GATEWAY,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_error(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ValueError)
    async def value_error(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
