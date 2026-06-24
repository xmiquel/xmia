## Context

The chart currently renders OHLCV candlesticks via Lightweight Charts. The user can see price movements visually but cannot inspect exact values of individual bars. MT5's built-in Data Window shows Date, Time, Open, High, Low, Close, Volume, Tick Volume, and Spread when hovering over a bar. This design adds an equivalent overlay.

The backend `get_rates()` currently returns only `time`, `open`, `high`, `low`, `close`, `volume` (which is actually MT5's `tick_volume`). MT5's `MqlRates` struct provides `tick_volume`, `spread`, and `real_volume` per candle, but these are discarded.

## Goals / Non-Goals

**Goals:**
- Display a floating data window on the chart when the user hovers over a candlestick
- Show: Date, Time, Open, High, Low, Close, Volume, Tick Volume, Spread
- Update the data window position and values in real-time as the user moves the crosshair
- Add `tick_volume`, `spread`, and `real_volume` to the backend rates response
- Style the data window to match the MT5 look (dark background, monospace data, label:value pairs)
- Update fake adapter to generate plausible values for the new fields

**Non-Goals:**
- No click interaction on the data window (read-only display)
- No persistence of hover state across page navigation
- No multi-symbol comparison in the data window
- No data window for non-OHLCV chart types (line, bar)
- No changes to the existing crosshair behavior

## Decisions

### 1. Backend: Add extra fields to rates response

- **MT5 returns** `MqlRates` arrays with fields: time, open, high, low, close, tick_volume, spread, real_volume
- **Current code** only extracts indices 0–5 (`tick_volume` as `volume`)
- **Decision**: Extract indices 5 (tick_volume), 6 (spread), and 7 (real_volume) and include them in the response
- **Backwards compatibility**: The old `volume` key is replaced with explicit `tick_volume` and `real_volume`. The frontend `Candle` type already defines `volume` — this will be retained as a convenience alias but the backend will explicitly name both.

### 2. Frontend: Lightweight Charts `crosshairMoved` event

- Lightweight Charts fires a `crosshairMoved` event with a `param` object containing `time` and `point`
- **Decision**: Subscribe to `crosshairMoved` on the chart instance, look up the nearest candle by `time` from the current data array, and render an HTML overlay positioned near the crosshair
- **Alternative considered**: Custom PaneView or Primitive — rejected because an HTML overlay is simpler to style, test, and maintain

### 3. Data window positioning

- **Decision**: Render the overlay as an HTML `div` positioned inside the chart container with `position: absolute`. Calculate x/y from the crosshair `point`. Clamp to viewport bounds so the tooltip doesn't overflow the chart edges.
- **Position**: Display to the right of the crosshair when possible; fall back to the left when near the right edge. Display above when near the bottom edge.

### 4. Data window styling

- Follow MT5's Data Window layout:
  - Dark semi-transparent background (`rgba(0,0,0,0.85)`)
  - White monospace text
  - Two columns: label (left-aligned) and value (right-aligned)
  - Fields separated by thin horizontal rules
  - Compact padding

### 5. Fake adapter updates

- Generate `tick_volume` and `real_volume` as random integers varying around the current `volume` value
- Generate `spread` as a small integer (1–20) with slight variation per candle (realistic for forex)

## Risks / Trade-offs

- **Performance**: `crosshairMoved` fires on every pixel of mouse movement. The lookup and DOM update must be lightweight. → Mitigation: use a hash map (`Map<time, Candle>`) for O(1) lookup instead of scanning the array each time.
- **Canvas vs DOM**: Lightweight Charts renders on Canvas; the data window is a DOM element. On rapid mouse movement, the overlay may feel slightly behind the canvas crosshair. → Mitigation: use `transform: translate()` for GPU-accelerated positioning.
- **Bar spacing**: If no candle exists at the crosshair time (gaps in data), the tooltip should hide rather than showing stale/empty data. → Mitigation: check that the resolved candle exists before rendering.
- **Backwards compat**: Existing frontend consumers of the rates API will now get extra fields. This is safe (no breaking changes) as extra JSON fields are ignored by existing clients.
