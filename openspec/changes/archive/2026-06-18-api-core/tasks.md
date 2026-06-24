## 1. Project Scaffolding

- [x] 1.1 Create `src/api/__init__.py`, `src/api/routers/__init__.py`, `src/api/services/__init__.py`, and `tests/api/__init__.py` package files
- [x] 1.2 Create `src/api/main.py` with FastAPI app factory (`create_app`), lifespan context manager for MT5 adapter lifecycle, and `/health` endpoint

## 2. API Key Authentication

- [x] 2.1 Create `src/api/dependencies.py` with `verify_api_key` dependency (reads `API_KEY` env var, validates `X-API-Key` header, bypasses auth when env var is unset) and `get_adapter` dependency (returns adapter from `app.state`)
- [x] 2.2 Write tests for auth: valid key, missing key, wrong key, dev mode (no key configured), health endpoint always public

## 3. HTTP Error Handling

- [x] 3.1 Create `src/api/errors.py` with `add_error_handlers(app)` that registers exception handlers mapping MT5 errors to HTTP status codes (503, 502, 401, 400, 500)
- [x] 3.2 Write tests verifying each MT5 error type returns the correct HTTP status and error format
- [x] 3.3 Integrate error handlers into the FastAPI app factory in `main.py`

## 4. Test Infrastructure

- [x] 4.1 Create `tests/api/conftest.py` with `fake_adapter` fixture (authenticated `FakeMT5Adapter`) and `client` fixture (`TestClient` with `app.dependency_overrides` for adapter injection)
- [x] 4.2 Verify test fixtures work by running a health check test

## 5. Timeframe Mapping

- [x] 5.1 Create `src/api/timeframes.py` with `TIMEFRAMES` dict mapping string constants to MT5 integer values (PERIOD_M1 through PERIOD_MN1) and `parse_timeframe(name)` function
- [x] 5.2 Write tests for valid timeframe mapping, invalid timeframe error

## 6. Account Endpoint

- [x] 6.1 Create `src/api/services/account_service.py` with `AccountService.get_account_info()` returning dict with all AccountInfo fields
- [x] 6.2 Create `src/api/routers/account.py` with `GET /api/v1/account` endpoint
- [x] 6.3 Register account router in main.py
- [x] 6.4 Write tests: successful account info, disconnected state returns 503

## 7. Symbol Info Endpoint

- [x] 7.1 Create `src/api/services/symbols_service.py` with `SymbolsService.get_symbol_info(symbol)` returning symbol metadata or raising 404
- [x] 7.2 Create `src/api/routers/symbols.py` with `GET /api/v1/symbols/{symbol}` endpoint
- [x] 7.3 Register symbols router in main.py
- [x] 7.4 Write tests: existing symbol, non-existent symbol (404), disconnected state (503)

## 8. Market Rates Endpoint

- [x] 8.1 Create `src/api/services/rates_service.py` with `RatesService.get_rates(symbol, timeframe, count)` using `parse_timeframe()` and returning OHLCV data
- [x] 8.2 Create `src/api/routers/rates.py` with `GET /api/v1/rates/{symbol}` endpoint with `timeframe` (default PERIOD_H1) and `count` (default 10, max 1000) query params
- [x] 8.3 Register rates router in main.py
- [x] 8.4 Write tests: default params, custom params, count exceeding max (422), invalid timeframe (422), disconnected state (503)

## 9. Final Verification

- [x] 9.1 Run full test suite: `uv run pytest tests/ -v --cov=src --cov-report=term-missing`
- [x] 9.2 Verify all existing MT5 adapter tests still pass and new API tests pass with coverage
