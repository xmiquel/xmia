## Why

The Watchlist currently shows three hardcoded symbols (`EURUSD`, `GBPUSD`, `BTCUSD`). Users should see the symbols actually available in their MT5 terminal — only the ones visible in Market Watch for now. This is the first step toward full symbol management (search, activate, etc.).

## What Changes

- **Backend**: New `get_symbols()` method on the MT5 adapter protocol that returns visible symbol names. New `GET /api/v1/symbols` REST endpoint returning the list.
- **Frontend**: `Layout.tsx` fetches the symbol list on mount and passes it to `Watchlist` instead of the hardcoded `DEFAULT_SYMBOLS`. `Watchlist.tsx` stays unchanged.
- **Fake adapter**: Returns a representative set of ~5 forex symbols for testing.
- **Live adapter**: Calls `mt5.symbols_get()` and returns only symbols where `visible == True`.

## Capabilities

### New Capabilities
- `symbols-list`: endpoint and adapter method to retrieve visible MT5 symbols as a flat string list

### Modified Capabilities
- `api-core`: add `GET /api/v1/symbols` endpoint (no authentication, returns `["EURUSD", "GBPUSD", ...]`)

## Impact

- `src/mt5/protocol.py` — add `get_symbols() -> list[str]`
- `src/mt5/live.py` — implement `get_symbols()` via `mt5.symbols_get()`
- `src/mt5/fake.py` — implement `get_symbols()` with known symbols
- `src/api/services/symbols_service.py` — add `get_symbols()`
- `src/api/routers/symbols.py` — add `GET /api/v1/symbols` route
- `frontend/src/api/symbols.ts` — add `getSymbols()` function
- `frontend/src/components/Layout.tsx` — replace `DEFAULT_SYMBOLS` with dynamic fetch
- `tests/` — new tests for protocol, fake, endpoint, and frontend
- No changes to PriceChart, AccountSummary, DataWindow, TimeframeSelector
