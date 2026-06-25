# Infinite Scroll

Automatic loading of historical candlestick data when the user drags the chart to the left, approaching the edge of loaded data.

---

## Requirement: Historical data loads on scroll

The chart SHALL detect when the user's visible range approaches the left edge of the loaded data. When the visible range is within 15% of the total bars, the system SHALL fetch the next 500 older candles from the API and append them to the chart.

### Scenario: Scroll left triggers data load

- **GIVEN** the chart has 500 candles loaded for EURUSD, PERIOD_H1
- **WHEN** the user drags the chart left such that the first visible bar is within the first 75 bars (15% of 500)
- **THEN** the system SHALL call `GET /api/v1/rates/EURUSD?timeframe=PERIOD_H1&count=500&before={earliest_candle_time}`
- **AND** SHALL prepend the returned candles to the chart data
- **AND** the visible range SHALL remain stable (user does not jump to a different position)

### Scenario: Empty response stops further loading

- **GIVEN** the user has scrolled to the earliest available data
- **WHEN** the `before` request returns an empty array
- **THEN** the system SHALL NOT make further requests when the user continues scrolling left
- **AND** no UI indicator SHALL be shown

### Scenario: No duplicate requests while loading

- **GIVEN** a `before` request is in flight
- **WHEN** the visible range enters the threshold zone
- **THEN** the system SHALL NOT initiate a duplicate request
- **AND** SHALL wait for the in-flight request to complete

### Scenario: Polling does not reset accumulated data

- **GIVEN** the chart has accumulated historical data from scrolling
- **WHEN** the 10-second polling interval fires and fetches the most recent candles
- **THEN** the accumulated historical data SHALL remain visible
- **AND** only the latest portion of data SHALL be updated

---

## Requirement: Silent loading (TradingView-style)

The infinite scroll SHALL NOT display loading spinners, skeletons, or any progress indicators. Old data SHALL appear in the chart silently when the API response arrives.

### Scenario: No loading indicator shown

- **GIVEN** a `before` request is in flight
- **WHEN** the user looks at the chart
- **THEN** no loading indicator of any kind SHALL be visible
- **AND** the chart SHALL remain interactive

---

## Requirement: Edge threshold

The 15% threshold SHALL be calculated based on the total number of loaded bars at the time of the scroll event.

### Scenario: Threshold scales with data volume

- **GIVEN** the chart has 1000 accumulated candles
- **WHEN** the first visible bar index is <= 150
- **THEN** the system SHALL trigger a data load
- **AND** when the first visible bar index is > 150, no load SHALL be triggered

---

## Non-Goals (v1)

- Forward scroll loading (existing polling covers real-time updates)
- Loading indicators or progress states
- Manual "load more" button
- Candle deduplication across polling and infinite scroll (acceptable for v1)
- Backend caching layer
- Maximum accumulated candle limit
