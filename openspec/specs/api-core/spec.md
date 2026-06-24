# API Core

REST API layer built on FastAPI, exposing MT5 data and trading operations via HTTP endpoints. This spec covers the initial iteration with account, symbol, and rate endpoints.

---

## Requirement: REST API Server

The system SHALL provide a FastAPI application that serves as the HTTP interface to MT5 functionality. The server SHALL manage the MT5 adapter lifecycle (initialize on startup, shutdown on stop). The adapter instance SHALL be injectable via FastAPI dependencies to support testing with fake adapters.

### Scenario: Application starts and connects to MT5
- **WHEN** the FastAPI application starts
- **THEN** it SHALL initialize the LiveMT5Adapter with configuration from MT5Config
- **AND** the adapter SHALL remain available for the lifetime of the application

### Scenario: Application stops and disconnects MT5
- **WHEN** the FastAPI application stops
- **THEN** it SHALL call shutdown() on the adapter
- **AND** release all MT5 resources

### Scenario: Adapter injection for testing
- **WHEN** a test overrides the adapter dependency
- **THEN** the application SHALL use the injected adapter (e.g., FakeMT5Adapter)
- **AND** the test SHALL NOT require a live MT5 terminal

---

## Requirement: API Key Authentication

The system SHALL support optional authentication via a static API key. The API key SHALL be configurable via the `API_KEY` environment variable. When `API_KEY` is not set, authentication SHALL be disabled (development mode). Protected endpoints SHALL reject requests with missing or invalid API keys.

### Scenario: API key configured and valid
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request includes the header `X-API-Key: sk-test123`
- **THEN** the request SHALL proceed normally

### Scenario: API key configured but missing
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request does NOT include the `X-API-Key` header
- **THEN** the server SHALL return HTTP 401 Unauthorized

### Scenario: API key configured but invalid
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request includes `X-API-Key: wrong-key`
- **THEN** the server SHALL return HTTP 401 Unauthorized

### Scenario: API key not configured (development mode)
- **GIVEN** `API_KEY` is NOT set
- **WHEN** any request is made without an API key
- **THEN** the request SHALL proceed normally (no authentication)

### Scenario: Health endpoint is always public
- **WHEN** a GET request is made to `/health`
- **THEN** the endpoint SHALL respond with HTTP 200 regardless of API key configuration or presence

---

## Requirement: Account Endpoint

The system SHALL expose a `GET /api/v1/account` endpoint that returns the current MT5 account information. The endpoint SHALL require authentication if API_KEY is configured.

**Response schema:**

```json
{
  "balance": 10000.00,
  "equity": 9500.00,
  "margin": 500.00,
  "free_margin": 9000.00,
  "margin_level": 1900.00,
  "currency": "USD",
  "name": "Demo Account",
  "server": "MetaQuotes-Demo",
  "leverage": 100
}
```

### Scenario: Get account info when authenticated
- **GIVEN** the adapter is in authenticated state
- **WHEN** a GET request is made to `/api/v1/account` with valid API key
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain all AccountInfo fields (balance, equity, margin, free_margin, margin_level, currency, name, server, leverage)

### Scenario: Get account info without authentication
- **GIVEN** the adapter is NOT authenticated
- **WHEN** a GET request is made to `/api/v1/account`
- **THEN** the response SHALL return HTTP 503 Service Unavailable
- **AND** the body SHALL indicate the adapter is not connected

---

## Requirement: Symbol Info Endpoint

The system SHALL expose a `GET /api/v1/symbols/{symbol}` endpoint that returns metadata for a given trading symbol.

**Response schema:**

```json
{
  "symbol": "EURUSD",
  "digits": 5,
  "spread": 10,
  "margin_currency": "EUR",
  "contract_size": 100000
}
```

### Scenario: Get info for existing symbol
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/symbols/EURUSD`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain digits, spread, margin_currency, and contract_size for EURUSD

### Scenario: Get info for non-existent symbol
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/symbols/INVALID`
- **THEN** the response SHALL return HTTP 404 Not Found

### Scenario: Get symbol info when not connected
- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/symbols/EURUSD`
- **THEN** the response SHALL return HTTP 503 Service Unavailable

---

## Requirement: Market Rates Endpoint

The system SHALL expose a `GET /api/v1/rates/{symbol}` endpoint that returns historical rate data (OHLCV candles) for a given symbol. Each candle SHALL include time, open, high, low, close, tick_volume, spread, and real_volume fields.

**Query parameters:**

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `timeframe` | string | `PERIOD_H1` | — | MT5 timeframe constant (PERIOD_M1, PERIOD_M3, PERIOD_M5, PERIOD_M6, PERIOD_M12, PERIOD_M15, PERIOD_M24, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1) |
| `count` | integer | 10 | 1000 | Number of candles to return |

**Response schema:**

```json
[
  {
    "time": 1780272000,
    "open": 1.1000,
    "high": 1.1005,
    "low": 1.0995,
    "close": 1.1002,
    "tick_volume": 150,
    "spread": 10,
    "real_volume": 150000
  }
]
```

### Scenario: Get rates for symbol with defaults
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL be an array of candles
- **AND** each candle SHALL have time, open, high, low, close, tick_volume, spread, and real_volume fields
- **AND** the array SHALL contain 10 candles by default

### Scenario: Get rates with custom timeframe and count
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=PERIOD_M5&count=5`
- **THEN** the response SHALL return 5 candles at M5 timeframe

### Scenario: Get rates with count exceeding maximum
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?count=2000`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity
- **AND** the error SHALL indicate count must not exceed 1000

### Scenario: Get rates with invalid timeframe
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=INVALID`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity

### Scenario: Get rates when not connected
- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 503 Service Unavailable

---

## Requirement: Timeframe Mapping

The system SHALL map string timeframe constants to MT5 integer constants. Supported mappings:

| String | MT5 Constant | Value | Notes |
|--------|-------------|-------|-------|
| `PERIOD_M1` | `TIMEFRAME_M1` | 1 | 1 minute |
| `PERIOD_M3` | `TIMEFRAME_M3` | 3 | 3 minutes |
| `PERIOD_M5` | `TIMEFRAME_M5` | 5 | 5 minutes |
| `PERIOD_M6` | `TIMEFRAME_M6` | 6 | 6 minutes |
| `PERIOD_M12` | `TIMEFRAME_M12` | 12 | 12 minutes |
| `PERIOD_M15` | `TIMEFRAME_M15` | 15 | 15 minutes |
| `PERIOD_M24` | `TIMEFRAME_M24` | 24 | 24 minutes |
| `PERIOD_M30` | `TIMEFRAME_M30` | 30 | 30 minutes |
| `PERIOD_H1` | `TIMEFRAME_H1` | 60 | 1 hour |
| `PERIOD_H4` | `TIMEFRAME_H4` | 240 | 4 hours |
| `PERIOD_D1` | `TIMEFRAME_D1` | 1440 | 1 day |
| `PERIOD_W1` | `TIMEFRAME_W1` | 10080 | 1 week |
| `PERIOD_MN1` | `TIMEFRAME_MN1` | 43200 | 1 month |

### Scenario: Valid timeframe string maps to integer
- **WHEN** the string `"PERIOD_H1"` is mapped
- **THEN** it SHALL return the integer value 60

### Scenario: Invalid timeframe string raises error
- **WHEN** an unrecognized timeframe string is provided
- **THEN** the system SHALL return HTTP 422 with a clear error message listing valid options

---

## Requirement: Error Handling

The system SHALL translate MT5 adapter errors into appropriate HTTP responses with consistent error format.

**Error response schema:**

```json
{
  "detail": "Human-readable error message"
}
```

| Adapter Error | HTTP Status | Description |
|--------------|-------------|-------------|
| `AdapterNotConnectedError` | 503 | Adapter not initialized or authenticated |
| `TerminalNotAvailableError` | 503 | MT5 terminal not available |
| `ConnectionError` | 502 | MT5 connection/operation failed |
| `AuthenticationError` | 401 | Invalid credentials |
| `ValueError` | 400 | Invalid request parameters |
| Any unhandled exception | 500 | Internal server error |

### Scenario: AdapterNotConnectedError returns 503
- **WHEN** the adapter raises AdapterNotConnectedError
- **THEN** the endpoint SHALL return HTTP 503 Service Unavailable
- **AND** the detail field SHALL contain the error message

### Scenario: Unhandled exception returns 500
- **WHEN** an unexpected exception occurs in the adapter
- **THEN** the endpoint SHALL return HTTP 500 Internal Server Error
- **AND** the detail field SHALL contain a generic error message (no stack traces exposed)

---

## Requirement: Health Check Endpoint

The system SHALL expose a `GET /health` endpoint for monitoring and load balancer checks. This endpoint SHALL NOT require authentication.

### Scenario: Health check returns OK
- **WHEN** a GET request is made to `/health`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain `{"status": "ok"}`

---

## Non-Goals (v1)

These features are explicitly deferred to future iterations:

- User registration and multi-tenancy
- JWT authentication
- Position and order management endpoints (POST/PATCH/DELETE)
- History endpoint
- WebSockets for real-time data
- Rate limiting or throttling
- Database persistence
- Docker containerization of the API (runs on Windows host)
