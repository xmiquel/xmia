## ADDED Requirements

### Requirement: List Symbols Endpoint

The system SHALL expose a `GET /api/v1/symbols` endpoint that returns the list of symbol names visible in the MT5 Market Watch. This endpoint SHALL NOT require authentication (same as health check).

**Response schema:**

```json
["EURUSD", "GBPUSD", "BTCUSD"]
```

#### Scenario: Get symbol list when connected

- **GIVEN** the adapter is connected
- **WHEN** a GET request is made to `/api/v1/symbols`
- **THEN** the response SHALL return HTTP 200
- **AND** the body SHALL be a JSON array of symbol name strings

#### Scenario: Get symbols when not connected

- **GIVEN** the adapter is NOT connected
- **WHEN** a GET request is made to `/api/v1/symbols`
- **THEN** the response SHALL return HTTP 503 Service Unavailable
