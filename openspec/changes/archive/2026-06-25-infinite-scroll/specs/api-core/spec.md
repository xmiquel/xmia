# API Core — Delta: Before Parameter

This spec extends the existing `GET /api/v1/rates/{symbol}` endpoint with an optional `before` parameter.

## New Requirement: Historical Rates via `before` Parameter

The system SHALL support an optional `before` query parameter on `GET /api/v1/rates/{symbol}`. When provided, the endpoint SHALL return `count` candles whose `time` is strictly less than the `before` timestamp, going backward from that point.

### Updated Request Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `timeframe` | string | `PERIOD_H1` | — | MT5 timeframe constant |
| `count` | integer | 10 | 1000 | Number of candles to return |
| `before` | integer (Unix seconds) | — | — | **New.** Return candles older than this timestamp |

### Scenario: Get rates before a timestamp

- **GIVEN** the adapter is connected
- **WHEN** a `GET` request is made to `/api/v1/rates/EURUSD?count=5&before=1800000000`
- **THEN** the response SHALL return `HTTP 200`
- **AND** the body SHALL be an array of up to 5 candles
- **AND** each candle SHALL have `time < 1800000000`

### Scenario: `before` timestamp filters correctly

- **WHEN** a request includes `before=1700000000`
- **THEN** all returned candles SHALL have `time` values strictly less than 1700000000

### Scenario: No more history available

- **GIVEN** there are no candles before the given `before` timestamp
- **WHEN** a request is made with `before`
- **THEN** the response SHALL return `HTTP 200`
- **AND** the body SHALL be an empty array `[]`

### Scenario: Invalid `before` value

- **WHEN** a request includes `before=invalid`
- **THEN** the server SHALL return `HTTP 422 Unprocessable Entity`

### Scenario: `before` with default count

- **WHEN** a request is made to `/api/v1/rates/EURUSD?before=1800000000` (without explicit `count`)
- **THEN** the response SHALL return 10 candles by default (existing default)
- **AND** all candles SHALL have `time < 1800000000`
