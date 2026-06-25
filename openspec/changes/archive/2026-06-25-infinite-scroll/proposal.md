## Why

The chart currently shows a fixed set of candles (100 by default). Users have no way to explore historical data by scrolling left. Unlike MT5 or TradingView, dragging the chart to the left hits a wall — no more data loads.

## What Changes

- Add `before` parameter to `GET /api/v1/rates/{symbol}` to fetch candles older than a given timestamp
- Add `get_rates_before` to the MT5 adapter protocol and implementations (`LiveMT5Adapter`, `FakeMT5Adapter`)
- Add `onVisibleRangeChange` callback to `PriceChart` component via `subscribeVisibleLogicalRangeChange`
- Add accumulated candle state in `Layout` to build up the history as the user scrolls
- Load 500 candles per batch when visible range is within 15% of the left edge
- No loading indicators — data appears silently like TradingView
- Forward (right) direction relies on existing 10s polling

## Capabilities

### New Capabilities
- `infinite-scroll`: Automatic historical data loading when dragging the chart left

### Modified Capabilities
- `api-core`: Add `before` query parameter to `GET /api/v1/rates/{symbol}`

## Impact

- **Backend**: `mt5/protocol.py`, `mt5/live.py`, `mt5/fake.py`, `api/routers/rates.py`, `api/services/rates_service.py` — add `get_rates_before` method and endpoint parameter
- **Frontend**: `PriceChart.tsx` — add `onVisibleRangeChange` prop; `Layout.tsx` — accumulated candle state, `handleVisibleRangeChange` callback; `api/rates.ts` — add `getRatesBeforeSymbol`
- **Tests**: Update backend tests for new endpoint parameter; update `PriceChart.test.tsx` and `Layout.test.tsx`
