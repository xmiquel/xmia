## Context

The PriceChart component shows candlestick data from the most recent N candles. Users who want to inspect older data have no way to load it — they see a fixed window. MT5 and TradingView both support dragging the chart left to reveal more history.

The backend uses `mt5.copy_rates_from_pos(symbol, tf, 0, count)` which always starts from the most recent candle. MT5 also provides `mt5.copy_rates_from(symbol, tf, date_from, count)` which returns `count` candles whose latest timestamp is <= `date_from`, going backward.

## Goals / Non-Goals

**Goals:**
- Allow users to drag the chart left and see more historical candles load automatically
- Load 500 candles per batch, with a 15% edge threshold (like TradingView)
- Silent loading — no spinners, data appears when ready
- Frontend accumulates candles in state; PriceChart only renders what it receives
- Backend exposes a `before` parameter on the rates endpoint

**Non-Goals:**
- No forward/right infinite scroll (existing polling handles updates)
- No changes to the chart library or rendering approach
- No UI indicators for loading state
- No position/order management changes

## Decisions

**Backend: `get_rates_before` method on MT5Adapter protocol**

A new method `get_rates_before(symbol, timeframe, count, before)` uses `mt5.copy_rates_from()` which returns candles older than the given timestamp. The result is filtered to exclude the exact `before` candle to avoid duplicates. The HTTP endpoint gets an optional `before` query parameter; when absent, behavior is unchanged.

**Frontend: Layout as the accumulator, PriceChart as the emitter**

The existing pattern (Layout orchestrates, PriceChart renders) stays. Layout:
- Maintains `allCandles[]` (accumulated) instead of a single `candles[]` batch
- Passes `onVisibleRangeChange` callback to PriceChart
- When `from` is within 15% of the left edge, calls `getRatesBeforeSymbol()` and prepends result to `allCandles`
- PriceChart subscribes to `subscribeVisibleLogicalRangeChange` on mount and calls the callback whenever the visible range changes

**Edge threshold: 15%**

Calculated as `visibleRange.from <= totalBars * 0.15`. When the first visible candle is within the first 15% of the accumulated data, a fetch is triggered. A `hasMore` flag prevents repeated calls once the backend returns an empty batch (no more historical data). An `isLoadingMore` guard prevents duplicate concurrent requests.

**Data merge strategy**

When older candles arrive, `setAllCandles(prev => [...olderCandles, ...prev])` prepends them. Lightweight Charts' `setData()` replaces all data, then `setVisibleLogicalRange()` restores the viewport so the user stays at the same logical position (shifted by the count of new bars).

When polling fires, its latest 100 candles merge into `allCandles` on the right side:

```ts
const mergeLatest = (existing: Candle[], incoming: Candle[]): Candle[] => {
  const existingTimes = new Set(existing.map(c => c.time));
  const newCandles = incoming.filter(c => !existingTimes.has(c.time));
  return [...existing, ...newCandles].sort((a, b) => Number(a.time) - Number(b.time));
};
```

## Risks / Trade-offs

- **Duplicate candles at boundary**: The `before` parameter is exclusive (time < before), so there's no overlap. This is enforced in both the live adapter (filter `int(r[0]) < before`) and the fake adapter.
- **Lightweight Charts re-render on setData**: Replacing all data with `setData()` is O(n) in the chart. With accumulated data growing unboundedly, this could get slow. Mitigation: users typically scroll through ~2000 candles before hitting the MT5 limit; acceptable for v1. If performance becomes an issue, use `setData()` only on the new slice + update approach.
- **Polling vs accumulated data**: When the polling interval (10s) fires, it fetches the latest 100 candles. The polling result SHALL be merged into `allCandles` — candles with existing timestamps are replaced, and truly new candles are appended at the right end. Since polling returns the most recent data and infinite scroll loads older data, there is minimal overlap (at most 1 candle at the boundary). A simple merge: filter incoming candles by `time` not already in `allCandles`, then concat and sort.

## Testing Strategy

- **Backend unit tests**: Test `get_rates_before` with the fake adapter — verify correct count, all timestamps < before, and empty response when no data exists.
- **Backend API tests**: Test `GET /api/v1/rates/EURUSD?count=5&before=1800000000` returns expected shape.
- **Frontend PriceChart tests**: Test that `onVisibleRangeChange` is called when the visible range changes. Mock `subscribeVisibleLogicalRangeChange` on the chart instance.
- **Frontend Layout tests**: Mock `getRatesBeforeSymbol`, trigger the callback with `from` within threshold, verify the mock was called with correct params.

## Files Changed

| File | Change |
|------|--------|
| `src/mt5/protocol.py` | Add `get_rates_before` to MT5Adapter protocol |
| `src/mt5/live.py` | Implement `get_rates_before` using `copy_rates_from` |
| `src/mt5/fake.py` | Implement `get_rates_before` for testing |
| `src/api/services/rates_service.py` | Add `get_rates_before` service method |
| `src/api/routers/rates.py` | Add `before` query parameter to `get_rates` endpoint |
| `frontend/src/types.ts` | Add `before` to Candle type if needed (already has `time`) |
| `frontend/src/api/rates.ts` | Add `getRatesBeforeSymbol` function |
| `frontend/src/components/PriceChart.tsx` | Add `onVisibleRangeChange` prop, subscribe to `subscribeVisibleLogicalRangeChange` |
| `frontend/src/components/Layout.tsx` | Replace `candles` with `allCandles` accumulation, add `handleVisibleRangeChange`, update `fetchRates` to merge into `allCandles` |
| `frontend/tests/api/client.test.ts` | Optional — no changes expected |
| `frontend/tests/components/PriceChart.test.tsx` | Add test for `onVisibleRangeChange` |
| `frontend/tests/components/Layout.test.tsx` | Add test for infinite scroll loading |
