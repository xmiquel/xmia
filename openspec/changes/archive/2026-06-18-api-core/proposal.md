## Why

The MT5 adapter layer (port/adapter) is complete, but there is no way to consume MT5 data from external tools, scripts, or a future frontend. The project is called "mi-api" and FastAPI is already declared as a dependency in `pyproject.toml`, yet no HTTP endpoints exist. Building the REST API layer is the natural next step to unlock integration with monitoring dashboards, trading bots, and web UIs.

## What Changes

- New `src/api/` package with FastAPI application, routers, services, and error handling
- Three read-only endpoints: account info, symbol metadata, and market rates (OHLCV)
- Optional API key authentication via `X-API-Key` header (disabled in dev mode)
- MT5 adapter lifecycle: initialize on startup, shutdown on stop
- Timeframe string-to-constant mapping for the rates endpoint
- HTTP error handlers that translate MT5 adapter exceptions to proper HTTP status codes

## Capabilities

### New Capabilities
- `api-core`: REST API layer exposing MT5 account info (`GET /api/v1/account`), symbol info (`GET /api/v1/symbols/{symbol}`), and market rates (`GET /api/v1/rates/{symbol}`) via FastAPI. Includes API key auth, MT5 lifecycle management, timeframe mapping, and error handling.

### Modified Capabilities
- *(none — no existing specs are being modified)*

## Impact

- **New package**: `src/api/` — FastAPI app, routers, services, dependencies, error handlers, timeframe mapping
- **New tests**: `tests/api/` — test client fixture, endpoint tests for account/symbols/rates
- **Dependencies**: `httpx` needed for testing (via `TestClient`), already pulled by FastAPI
- **Configuration**: Optional `API_KEY` env var for authentication; `MT5_*` env vars already exist from MT5 config
- **No Docker impact**: API runs on Windows host alongside MT5 terminal
