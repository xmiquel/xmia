## ADDED Requirements

### Requirement: Chart shows price with correct decimal precision per symbol
The chart SHALL display price labels (crosshair, axis) with the number of decimal places matching the symbol's `digits` value from the symbol info API. For example, EURUSD (digits=5) SHALL show prices like `1.10000`, not `1.10`.

#### Scenario: EURUSD shows 5 decimal places
- **GIVEN** the selected symbol is `EURUSD`
- **AND** the backend returns `digits: 5` for EURUSD
- **WHEN** the chart renders candlestick data
- **THEN** the price axis labels and crosshair price SHALL display values with 5 decimal places (e.g., `1.10000`)

#### Scenario: fallback precision when symbol info unavailable
- **GIVEN** the backend returns an error for symbol info
- **WHEN** the chart renders
- **THEN** the chart SHALL use a default of 5 decimal places

### Requirement: Time scale shows HH:mm for intraday timeframes
The chart time scale SHALL display time labels in `HH:mm` format in addition to the date when using intraday timeframes (PERIOD_M1 through PERIOD_H4). Seconds SHALL NOT be shown.

#### Scenario: M1 timeframe shows time
- **GIVEN** the selected timeframe is `PERIOD_M1`
- **WHEN** the chart renders candlestick data with UNIX timestamps
- **THEN** the time scale SHALL display labels with date and `HH:mm` (e.g., `2026-06-24 14:30`)
- **AND** seconds SHALL NOT be visible

#### Scenario: D1 timeframe still shows date only
- **GIVEN** the selected timeframe is `PERIOD_D1`
- **WHEN** the chart renders
- **THEN** the time scale SHALL still work correctly (time component shows `00:00`)

### Requirement: Price scale (y-axis) labels are visible
The y-axis price scale SHALL display tick labels with values matching the price data range and the symbol's decimal precision.

#### Scenario: price scale shows labels
- **GIVEN** candlestick data is loaded for EURUSD
- **WHEN** the chart renders
- **THEN** the right-side price scale SHALL display numeric labels at regular intervals
- **AND** each label SHALL use the same decimal precision as the symbol
