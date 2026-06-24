## Why

The current chart shows candlestick data visually but provides no way to inspect the exact OHLCV values, tick volume, or spread of individual bars. MT5's built-in Data Window displays these details on hover, and users of this dashboard need the same capability for analysis and verification.

## What Changes

- **Backend**: Add `tick_volume`, `spread`, and `real_volume` fields to the `GET /api/v1/rates/{symbol}` response. The current `volume` field maps to MT5's `tick_volume` (index 5), which is misleading — we will expose all three fields explicitly.
- **Frontend**: Update the `Candle` type to include `tick_volume`, `spread`, and `real_volume`. Implement a floating data window (tooltip) on `PriceChart` that appears when hovering over a candlestick, displaying Date, Time, Open, High, Low, Close, Volume, Tick Volume, and Spread — styled similarly to MT5's Data Window.
- **Fake adapter**: Update `get_rates()` to generate and return realistic `tick_volume`, `real_volume`, and `spread` values.

## Capabilities

### New Capabilities
- `data-window`: Floating tooltip overlay on the candlestick chart that shows per-bar details (Date, Time, OHLCV, Tick Volume, Spread) on hover, matching the layout and information density of the MT5 Data Window.

### Modified Capabilities
- `api-core` (Market Rates Endpoint): The rate response schema will gain three new fields (`tick_volume`, `spread`, `real_volume`). The existing `volume` field remains but is renamed to `tick_volume` for clarity.
- `chart-formatting`: No requirement changes (data window is a new component, not a formatting change).

## Impact

- **Backend**: `src/mt5/live.py` — `get_rates()` returns additional fields. `src/mt5/fake.py` — generates fake tick_volume, real_volume, spread. `src/api/services/rates_service.py` — passes through new fields (no transformation needed). `tests/` — update contract, live, and fake tests for new fields.
- **Frontend**: `src/types.ts` — `Candle` interface gains optional `tick_volume`, `spread`, `real_volume`. `src/components/PriceChart.tsx` — new crosshair tooltip overlay using lightweight charts `crosshairMoved` event. New CSS for tooltip positioning and styling. `tests/` — tooltip rendering tests.
