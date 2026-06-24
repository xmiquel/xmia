## Why

The chart currently shows price labels with only 2 decimal places (e.g., 1.10 instead of 1.10000 for EURUSD), the time scale lacks HH:mm labels for intraday timeframes, and the price scale (y-axis) doesn't show any values. These formatting gaps make the chart hard to read and interpret for trading.

## What Changes

- Pass symbol digit count (`digits`) from `Layout` to `PriceChart` via `getSymbolInfo` API call
- Configure `priceFormat` on the candlestick series to match the symbol's precision (e.g., 5 digits for EURUSD)
- Enable `timeVisible` on the time scale so intraday timeframes show HH:mm labels
- Ensure the price scale (y-axis) renders correct tick labels by fixing the precision configuration

## Capabilities

### New Capabilities
- `chart-formatting`: Chart formatting configuration — price precision per symbol, time scale visibility, and price scale labels

### Modified Capabilities
*(none — existing specs unchanged)*

## Impact

- **Frontend**: `PriceChart.tsx` — add `digits` prop, configure `priceFormat` on candlestick series, enable `timeVisible` and `secondsVisible` on time scale
- **Frontend**: `Layout.tsx` — fetch `digits` from `getSymbolInfo()` on symbol change, pass to `PriceChart`
- **Tests**: Update `PriceChart.test.tsx` and `Layout.test.tsx` to pass `digits` prop in mocks
- No backend changes required
