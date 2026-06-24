def test_get_rates_default(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    candle = data[0]
    assert "time" in candle
    assert "open" in candle
    assert "high" in candle
    assert "low" in candle
    assert "close" in candle
    assert "volume" in candle


def test_get_rates_with_custom_params(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?timeframe=PERIOD_M5&count=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_get_rates_exceeds_max_count(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?count=2000")
    assert response.status_code == 422


def test_get_rates_invalid_timeframe(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?timeframe=INVALID")
    assert response.status_code == 422


def test_get_rates_when_disconnected(client, fake_adapter):
    fake_adapter.shutdown()
    response = client.get("/api/v1/rates/EURUSD")
    assert response.status_code == 503
