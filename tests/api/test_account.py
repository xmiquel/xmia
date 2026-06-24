def test_get_account_info(client, fake_adapter):
    response = client.get("/api/v1/account")
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 10000.0
    assert data["equity"] == 9500.0
    assert data["currency"] == "USD"
    assert data["name"] == "Fake Account"
    assert "margin_level" in data
    assert "leverage" in data


def test_get_account_info_when_disconnected(client, fake_adapter):
    fake_adapter.shutdown()
    response = client.get("/api/v1/account")
    assert response.status_code == 503
    assert "detail" in response.json()
