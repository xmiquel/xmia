from fastapi.testclient import TestClient

from mt5.fake import FakeMT5Adapter


def test_app_creates_successfully():
    from api.main import create_app

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)
    assert app is not None


def test_health_returns_ok():
    from api.main import create_app

    adapter = FakeMT5Adapter()
    adapter.initialize(login=1, password="p", server="s")
    app = create_app(adapter)
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
