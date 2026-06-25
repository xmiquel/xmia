### Task 2: Backend — Add `before` parameter to HTTP endpoint

**Files:**
- Modify: `src/api/services/rates_service.py:9-11`
- Modify: `src/api/routers/rates.py:23-31`
- Test: `tests/api/test_rates.py`

**Interfaces:**
- Consumes: `MT5Adapter.get_rates_before` from Task 1
- Produces: `GET /api/v1/rates/{symbol}?before={timestamp}` query parameter

- [ ] **Step 1: Add `get_rates_before` to `RatesService`**

In `src/api/services/rates_service.py`:

```python
def get_rates_before(self, symbol: str, timeframe: str, count: int, before: int) -> list[dict]:
    tf = parse_timeframe(timeframe)
    return self._adapter.get_rates_before(symbol, tf, count, before)
```

- [ ] **Step 2: Add `before` query parameter to endpoint**

Modify `src/api/routers/rates.py`:

```python
@router.get("/api/v1/rates/{symbol}")
async def get_rates(
    symbol: str = Path(..., min_length=1, max_length=20),
    timeframe: str = Depends(_validate_timeframe),
    count: int = Query(10, ge=1, le=1000, description="Number of candles (max 1000)"),
    before: int | None = Query(None, description="Unix timestamp (seconds). If provided, returns candles older than this timestamp."),
    adapter: MT5Adapter = Depends(get_adapter),
):
    service = RatesService(adapter)
    if before is not None:
        return service.get_rates_before(symbol, timeframe, count, before)
    return service.get_rates(symbol, timeframe, count)
```

- [ ] **Step 3: Write API tests**

Add to `tests/api/test_rates.py`:

```python
def test_get_rates_with_before(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?count=5&before=1800000000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for candle in data:
        assert candle["time"] < 1800000000


def test_get_rates_before_empty(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?count=5&before=1000000000")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_rates_invalid_before(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?before=notanumber")
    assert response.status_code == 422
```

- [ ] **Step 4: Run API tests**

Run: `uv run pytest tests/api/test_rates.py -v`
Expected: All 7 tests pass (4 existing + 3 new)

- [ ] **Step 5: Commit**

```bash
git add src/api/services/rates_service.py src/api/routers/rates.py tests/api/test_rates.py
git commit -m "feat: add before parameter to GET /api/v1/rates/{symbol}"
```
