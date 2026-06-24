import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mt5.errors import (
    AdapterNotConnectedError,
    AuthenticationError,
    ConnectionError,
    TerminalNotAvailableError,
)


@pytest.mark.parametrize(
    "exception, expected_status",
    [
        (AdapterNotConnectedError("not connected"), 503),
        (TerminalNotAvailableError("terminal not found"), 503),
        (ConnectionError("mt5 failed"), 502),
        (AuthenticationError("bad login"), 401),
        (ValueError("bad input"), 400),
        (RuntimeError("unexpected"), 500),
    ],
)
def test_error_handler_mapping(exception, expected_status):
    from api.errors import add_error_handlers

    app = FastAPI()
    add_error_handlers(app)

    @app.get("/error")
    async def trigger_error():
        raise exception

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/error")
    assert response.status_code == expected_status
