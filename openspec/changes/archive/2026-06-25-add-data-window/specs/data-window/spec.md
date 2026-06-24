## ADDED Requirements

### Requirement: Data window appears on candle hover

The chart SHALL display a floating data window overlay when the user hovers over a candlestick. The data window SHALL show per-bar details: Date, Time, Open, High, Low, Close, Volume, Tick Volume, and Spread. The window SHALL disappear when the crosshair leaves the chart area.

#### Scenario: hover over a candlestick shows data window
- **GIVEN** the chart displays candlestick data for EURUSD
- **WHEN** the user moves the mouse over a candlestick bar
- **THEN** a floating data window SHALL appear near the crosshair position
- **AND** the window SHALL display the Date, Time, Open, High, Low, Close, Volume, Tick Volume, and Spread of that bar
- **AND** the values SHALL match the actual data of the hovered candle

#### Scenario: data window hides when crosshair leaves chart
- **GIVEN** the data window is visible
- **WHEN** the mouse leaves the chart area
- **THEN** the data window SHALL disappear

#### Scenario: data window updates in real-time on hover
- **GIVEN** the data window is visible over one candle
- **WHEN** the user moves the mouse to a different candle
- **THEN** the data window SHALL update to show the values of the newly hovered candle
- **AND** the transition SHALL be instantaneous (no fade or delay)

### Requirement: Data window shows correct precision per symbol

All price values in the data window (Open, High, Low, Close) SHALL display with the number of decimal places matching the symbol's `digits` value.

#### Scenario: EURUSD shows 5 decimal places in data window
- **GIVEN** the selected symbol is EURUSD (digits=5)
- **WHEN** the data window is visible over a candle
- **THEN** Open, High, Low, and Close SHALL display with 5 decimal places (e.g., `1.10000`)

### Requirement: Data window follows MT5 Data Window layout

The data window SHALL visually resemble the MT5 Data Window: dark semi-transparent background, white monospace text, two-column label:value layout, compact spacing.

#### Scenario: data window displays label:value pairs
- **GIVEN** the data window is visible
- **THEN** each field SHALL display as a label colon value pair (e.g., `Open: 1.10000`)
- **AND** labels SHALL be left-aligned
- **AND** values SHALL be right-aligned
- **AND** the background SHALL be dark semi-transparent
- **AND** text SHALL be monospace white

### Requirement: Data window does not overflow chart

The data window SHALL clamp its position so it remains fully visible within the chart container bounds. If the crosshair is near the right edge, the window SHALL appear to the left of the crosshair. If near the bottom, it SHALL appear above.

#### Scenario: data window repositions when near edge
- **GIVEN** the crosshair is near the right edge of the chart
- **WHEN** the data window appears
- **THEN** the window SHALL be positioned to the left of the crosshair to avoid overflow
- **GIVEN** the crosshair is near the bottom edge of the chart
- **WHEN** the data window appears
- **THEN** the window SHALL be positioned above the crosshair to avoid overflow
