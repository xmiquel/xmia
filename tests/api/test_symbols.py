def test_get_symbol_info(client, fake_adapter):
    response = client.get("/api/v1/symbols/EURUSD")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "EURUSD"
    assert data["digits"] == 5
    assert data["spread"] == 10
    assert data["margin_currency"] == "EUR"
    assert data["contract_size"] == 100000


def test_get_symbol_info_not_found(client, fake_adapter):
    response = client.get("/api/v1/symbols/INVALID")
    assert response.status_code == 404


def test_get_symbol_info_when_disconnected(client, fake_adapter):
    fake_adapter.shutdown()
    response = client.get("/api/v1/symbols/EURUSD")
    assert response.status_code == 503
