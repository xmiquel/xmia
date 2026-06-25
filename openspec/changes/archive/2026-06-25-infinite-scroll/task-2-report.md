# Task 2 Report: Add `before` parameter to HTTP endpoint

## What was implemented

1. **`src/api/services/rates_service.py`** — Added `get_rates_before(symbol, timeframe, count, before)` method that delegates to adapter.

2. **`src/api/routers/rates.py`** — Added `before: int | None` query parameter to `GET /api/v1/rates/{symbol}`. When provided, calls `get_rates_before`; otherwise falls back to `get_rates`.

3. **`tests/api/test_rates.py`** — Added 3 new tests:
   - `test_get_rates_with_before` — verifies 5 candles returned all with `time < 1800000000`
   - `test_get_rates_before_empty` — verifies empty list for very old timestamp
   - `test_get_rates_invalid_before` — verifies 422 for non-integer `before`

4. **`src/mt5/fake.py`** — Added early return `[]` in `get_rates_before` when `before <= 1_000_000_000` (needed because the fake adapter otherwise always generates data and never returns empty).

## Test results

```
tests/api/test_rates.py ........                                     [100%]
8 passed in 0.11s
```
(5 existing + 3 new)

All 37 existing fake adapter tests also pass.

## Files changed

| File | Change |
|------|--------|
| `src/api/services/rates_service.py` | Added `get_rates_before` method |
| `src/api/routers/rates.py` | Added `before` query param + branching |
| `tests/api/test_rates.py` | 3 new tests |
| `src/mt5/fake.py` | Early return for old timestamps |

## Self-review

- The `before` parameter is correctly typed as `int | None` with FastAPI using strict validation (non-integer → 422).
- Routing logic is clean: single endpoint dispatches to `get_rates` or `get_rates_before` based on presence of `before`.
- The empty test required a minor change to `fake.py` (early return when `before <= 1_000_000_000`) because the fake adapter generates data for any timestamp, making an empty result impossible.

## Issues or concerns

None. All tests pass, commit made with the specified message.
