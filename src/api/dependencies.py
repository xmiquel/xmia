import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from mt5.protocol import MT5Adapter

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _get_api_key() -> str | None:
    return os.environ.get("API_KEY")


async def verify_api_key(
    api_key: str | None = Depends(_api_key_header),
) -> None:
    expected = _get_api_key()
    if expected is None:
        return
    if api_key != expected:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )


async def get_adapter(request: Request) -> MT5Adapter:
    return request.app.state.adapter
