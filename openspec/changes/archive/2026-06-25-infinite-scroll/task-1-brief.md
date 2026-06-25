### Task 1: Backend — Add `get_rates_before` to protocol and adapters

**Files:**
- Modify: `src/mt5/protocol.py:85-86`
- Modify: `src/mt5/live.py:145-167`
- Modify: `src/mt5/fake.py:145-164`
- Modify: `tests/test_protocol.py:9-23`
- Test: `tests/test_fake.py` (already read by test runner)

**Interfaces:**
- Consumes: `MT5Adapter` protocol (existing)
- Produces: `get_rates_before(symbol, timeframe, count, before) -> list[dict]` — returns candles with `time < before`

- [ ] **Step 1: Add `get_rates_before` to protocol**

In `src/mt5/protocol.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    ...
```

Also update `test_protocol.py` — add `"get_rates_before"` to the `expected_methods` list.

- [ ] **Step 2: Implement in `LiveMT5Adapter`**

In `src/mt5/live.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    mt5 = self._import_mt5()
    if not self._connected:
        raise AdapterNotConnectedError("Not connected")

    mt5.symbol_select(symbol, True)
    rates = mt5.copy_rates_from(symbol, timeframe, before, count)
    if rates is None:
        return []

    return [
        {
            "time": int(r[0]),
            "open": float(r[1]),
            "high": float(r[2]),
            "low": float(r[3]),
            "close": float(r[4]),
            "tick_volume": int(r[5]),
            "spread": int(r[6]),
            "real_volume": int(r[7]),
        }
        for r in rates
        if int(r[0]) < before
    ]
```

- [ ] **Step 3: Implement in `FakeMT5Adapter`**

In `src/mt5/fake.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    self._check_error("get_rates_before")
    self._require_state(AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

    rates = []
    current_time = before - 1
    for i in range(count):
        t = datetime.fromtimestamp(current_time) - timedelta(hours=timeframe * i)
        base = 1.1000 - (i * 0.0001)
        rates.append({
            "time": int(t.timestamp()),
            "open": base,
            "high": base + 0.0005,
            "low": base - 0.0005,
            "close": base + 0.0002,
            "tick_volume": 100 + i * 10,
            "spread": 5 + (i % 15),
            "real_volume": (100 + i * 10) * 1000,
        })
    return [r for r in rates if r["time"] < before]
```

- [ ] **Step 4: Run backend tests**

Run: `uv run pytest tests/test_fake.py tests/test_protocol.py -v`
Expected: All tests pass (including existing ones)

- [ ] **Step 5: Commit**

```bash
git add src/mt5/protocol.py src/mt5/live.py src/mt5/fake.py tests/test_protocol.py
git commit -m "feat: add get_rates_before to MT5 adapter protocol and implementations"
```
