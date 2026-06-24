import os

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient

from mt5.fake import FakeMT5Adapter


def test_verify_api_key_missing_when_configured():
    os.environ["API_KEY"] = "sk-test123"
    from api.main import create_app
    from api.dependencies import verify_api_key

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)

    @app.get("/protected")
    async def protected(_=Depends(verify_api_key)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected")
    assert response.status_code == 401
    del os.environ["API_KEY"]


def test_verify_api_key_valid():
    os.environ["API_KEY"] = "sk-test123"
    from api.main import create_app
    from api.dependencies import verify_api_key

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)

    @app.get("/protected")
    async def protected(_=Depends(verify_api_key)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected", headers={"X-API-Key": "sk-test123"})
    assert response.status_code == 200
    del os.environ["API_KEY"]


def test_verify_api_key_invalid():
    os.environ["API_KEY"] = "sk-test123"
    from api.main import create_app
    from api.dependencies import verify_api_key

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)

    @app.get("/protected")
    async def protected(_=Depends(verify_api_key)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    del os.environ["API_KEY"]


def test_verify_api_key_disabled_in_dev():
    os.environ.pop("API_KEY", None)
    from api.main import create_app
    from api.dependencies import verify_api_key

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)

    @app.get("/protected")
    async def protected(_=Depends(verify_api_key)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected")
    assert response.status_code == 200


def test_health_is_always_public():
    os.environ["API_KEY"] = "sk-test123"
    from api.main import create_app

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    del os.environ["API_KEY"]
