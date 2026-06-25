# Task 1 Report: Add `get_rates_before` to MT5 adapter protocol and implementations

## What I implemented

- **`src/mt5/protocol.py`**: Added `get_rates_before(symbol, timeframe, count, before) -> list[dict[str, object]]` method signature after `get_rates`
- **`src/mt5/live.py`**: Implemented `get_rates_before` using `mt5.copy_rates_from()` with `time < before` filtering and `AdapterNotConnectedError` guard
- **`src/mt5/fake.py`**: Implemented `get_rates_before` generating synthetic candles with times before the given `before` timestamp, with state checks and error simulation support
- **`tests/test_protocol.py`**: Added `"get_rates_before"` to `expected_methods` list
- **`tests/test_fake.py`**: Added 6 new test cases for `get_rates_before` (count, timestamp filtering, required fields, state guard, error mode)

## Test Results

```
43 passed in 0.09s
```

All existing tests pass + 6 new tests for `get_rates_before` on `FakeMT5Adapter`.

## Files Changed

| File | Change |
|------|--------|
| `src/mt5/protocol.py` | Added method signature (6 lines) |
| `src/mt5/live.py` | Added live implementation (23 lines) |
| `src/mt5/fake.py` | Added fake implementation (23 lines) |
| `tests/test_protocol.py` | Added to `expected_methods` list (1 line) |
| `tests/test_fake.py` | Added 6 test methods (53 lines) |

## Self-Review

- ✅ All spec steps completed (protocol → live → fake → tests → commit)
- ✅ Edge cases covered: disconnected state, error simulation, None/null response, time filtering
- ✅ Follows existing codebase patterns (state guards, error modes, same candle field names)
- ✅ Tests are clean with no warnings or noise
- ✅ Commit message matches conventional commit format

## Concerns

None.

## Commit

`9915dea` feat: add get_rates_before to MT5 adapter protocol and implementations
