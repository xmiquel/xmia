## MODIFIED Requirements

### Requirement: Market Rates Endpoint

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

#### Scenario: Get rates for symbol with defaults
- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL be an array of candles
- **AND** each candle SHALL have time, open, high, low, close, tick_volume, spread, and real_volume fields
- **AND** the array SHALL contain 10 candles by default

#### Scenario: Get rates with custom timeframe and count
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=PERIOD_M5&count=5`
- **THEN** the response SHALL return 5 candles at M5 timeframe

#### Scenario: Get rates with count exceeding maximum
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?count=2000`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity
- **AND** the error SHALL indicate count must not exceed 1000

#### Scenario: Get rates with invalid timeframe
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD?timeframe=INVALID`
- **THEN** the response SHALL return HTTP 422 Unprocessable Entity

#### Scenario: Get rates when not connected
- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/rates/EURUSD`
- **THEN** the response SHALL return HTTP 503 Service Unavailable
