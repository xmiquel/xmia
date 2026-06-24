## ADDED Requirements

### Requirement: REST API Server

The system SHALL provide a FastAPI application that serves as the HTTP interface to MT5 functionality. The server SHALL manage the MT5 adapter lifecycle (initialize on startup, shutdown on stop). The adapter instance SHALL be injectable via FastAPI dependencies to support testing with fake adapters.

#### Scenario: Application starts and connects to MT5
- **WHEN** the FastAPI application starts
- **THEN** it SHALL initialize the LiveMT5Adapter with configuration from MT5Config
- **AND** the adapter SHALL remain available for the lifetime of the application

#### Scenario: Application stops and disconnects MT5
- **WHEN** the FastAPI application stops
- **THEN** it SHALL call shutdown() on the adapter
- **AND** release all MT5 resources

#### Scenario: Adapter injection for testing
- **WHEN** a test overrides the adapter dependency
- **THEN** the application SHALL use the injected adapter (e.g., FakeMT5Adapter)
- **AND** the test SHALL NOT require a live MT5 terminal

---

### Requirement: API Key Authentication

The system SHALL support optional authentication via a static API key. The API key SHALL be configurable via the `API_KEY` environment variable. When `API_KEY` is not set, authentication SHALL be disabled (development mode). Protected endpoints SHALL reject requests with missing or invalid API keys.

#### Scenario: API key configured and valid
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request includes the header `X-API-Key: sk-test123`
- **THEN** the request SHALL proceed normally

#### Scenario: API key configured but missing
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request does NOT include the `X-API-Key` header
- **THEN** the server SHALL return HTTP 401 Unauthorized

#### Scenario: API key configured but invalid
- **GIVEN** `API_KEY` is set to `"sk-test123"`
- **WHEN** a request includes `X-API-Key: wrong-key`
- **THEN** the server SHALL return HTTP 401 Unauthorized

#### Scenario: API key not configured (development mode)
- **GIVEN** `API_KEY` is NOT set
- **WHEN** any request is made without an API key
- **THEN** the request SHALL proceed normally (no authentication)

#### Scenario: Health endpoint is always public
- **WHEN** a GET request is made to `/health`
- **THEN** the endpoint SHALL respond with HTTP 200 regardless of API key configuration or presence

---

### Requirement: Account Endpoint

The system SHALL expose a `GET /api/v1/account` endpoint that returns the current MT5 account information. The endpoint SHALL require authentication if API_KEY is configured.

#### Scenario: Get account info when authenticated
- **GIVEN** the adapter is in authenticated state
- **WHEN** a GET request is made to `/api/v1/account` with valid API key
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain balance, equity, margin, free_margin, margin_level, currency, name, server, and leverage fields

#### Scenario: Get account info without authentication
- **GIVEN** the adapter is NOT authenticated
- **WHEN** a GET request is made to `/api/v1/account`
- **THEN** the response SHALL return HTTP 503 Service Unavailable
- **AND** the body SHALL indicate the adapter is not connected

---

### Requirement: Symbol Info Endpoint

The system SHALL expose a `GET /api/v1/symbols/{symbol}` endpoint that returns metadata for a given trading symbol.

#### Scenario: Get info for existing symbol
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/symbols/EURUSD`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain digits, spread, margin_currency, and contract_size for EURUSD

#### Scenario: Get info for non-existent symbol
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/symbols/INVALID`
- **THEN** the response SHALL return HTTP 404 Not Found

#### Scenario: Get symbol info when not connected
- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/symbols/EURUSD`
- **THEN** the response SHALL return HTTP 503 Service Unavailable

---

### Requirement: Market Rates Endpoint

The system SHALL expose a `GET /api/v1/rates/{symbol}` endpoint that returns historical rate data (OHLCV candles) for a given symbol. The endpoint SHALL accept `timeframe` (string, default `PERIOD_H1`) and `count` (integer, default 10, max 1000) query parameters.

#### Scenario: Get rates for symbol with defaults
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL be an array of 10 candles
- **AND** each candle SHALL have time, open, high, low, close, and volume fields

#### Scenario: Get rates with custom timeframe and count
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=PERIOD_M5&count=5`
- **THEN** the response SHALL return 5 candles at M5 timeframe

#### Scenario: Get rates with count exceeding maximum
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?count=2000`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity

#### Scenario: Get rates with invalid timeframe
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=INVALID`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity

#### Scenario: Get rates when not connected
- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 503 Service Unavailable

---

### Requirement: Timeframe Mapping

The system SHALL map string timeframe constants to MT5 integer constants. Supported mappings: PERIOD_M1 (1), PERIOD_M3 (3), PERIOD_M5 (5), PERIOD_M6 (6), PERIOD_M12 (12), PERIOD_M15 (15), PERIOD_M24 (24), PERIOD_M30 (30), PERIOD_H1 (60), PERIOD_H4 (240), PERIOD_D1 (1440), PERIOD_W1 (10080), PERIOD_MN1 (43200).

#### Scenario: Valid timeframe string maps to integer
- **WHEN** the string `"PERIOD_H1"` is mapped
- **THEN** it SHALL return the integer value 60

#### Scenario: Invalid timeframe string raises error
- **WHEN** an unrecognized timeframe string is provided
- **THEN** the system SHALL return HTTP 422 with a clear error message listing valid options

---

### Requirement: Error Handling

The system SHALL translate MT5 adapter errors into appropriate HTTP responses with consistent error format. AdapterNotConnectedError and TerminalNotAvailableError SHALL return 503. ConnectionError SHALL return 502. AuthenticationError SHALL return 401. ValueError SHALL return 400. Unhandled exceptions SHALL return 500 with a generic message.

#### Scenario: AdapterNotConnectedError returns 503
- **WHEN** the adapter raises AdapterNotConnectedError
- **THEN** the endpoint SHALL return HTTP 503 Service Unavailable
- **AND** the detail field SHALL contain the error message

#### Scenario: Unhandled exception returns 500
- **WHEN** an unexpected exception occurs in the adapter
- **THEN** the endpoint SHALL return HTTP 500 Internal Server Error
- **AND** the detail field SHALL contain a generic error message

---

### Requirement: Health Check Endpoint

The system SHALL expose a `GET /health` endpoint for monitoring. This endpoint SHALL NOT require authentication.

#### Scenario: Health check returns OK
- **WHEN** a GET request is made to `/health`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL contain `{"status": "ok"}`
