import pytest
from fastapi.testclient import TestClient

from mt5.fake import FakeMT5Adapter


@pytest.fixture
def fake_adapter():
    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    return adapter


@pytest.fixture
def client(fake_adapter):
    from api.dependencies import get_adapter
    from api.main import create_app

    app = create_app(fake_adapter)
    app.dependency_overrides[get_adapter] = lambda: fake_adapter
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
