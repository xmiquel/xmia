## Context

The chart (`PriceChart` component) uses Lightweight Charts but lacks symbol-aware formatting. Price labels default to 2 decimal places regardless of the symbol's actual digit count (e.g., EURUSD should show 5 digits). The time scale only shows dates (yyyy-MM-dd) without HH:mm for intraday timeframes. The price scale y-axis labels render blanks due to mismatched precision.

The symbol's digit count is already available via `GET /api/v1/symbols/{symbol}` which returns a `digits` field.

## Goals / Non-Goals

**Goals:**
- Make price labels display the correct decimal precision per symbol (e.g., 5 digits for EURUSD, 3 for JPY pairs)
- Show HH:mm on the time scale for intraday timeframes (M1–H4)
- Render price scale (y-axis) tick labels correctly
- Keep changes scoped to the frontend — no backend modifications

**Non-Goals:**
- No server-side changes — the `digits` field already exists in the symbol API response
- No new API endpoints or data model changes
- No changes to the candlestick data structure (UNIX timestamps stay as-is)
- No localization/currency symbol formatting — just raw decimal precision

## Decisions

**Approach: fetch `digits` from symbol API on symbol change**

`Layout` already fetches account info and rates on a polling interval. Adding a `getSymbolInfo` call when the selected symbol changes is the natural extension. The `digits` value is passed as a prop to `PriceChart`, which uses it in the `priceFormat` option of the candlestick series.

Alternatives considered:
- **Hardcode a symbol→digits map on the frontend** — rejected because it would need maintenance and the backend already returns this data.
- **Include `digits` in the rates response** — rejected because it would couple pricing data with rate data and require backend changes.

**Price precision: `priceFormat.type = 'price'` with `precision` and `minMove`**

Lightweight Charts' `CandlestickSeries` accepts a `priceFormat` option where `precision` controls the number of decimal places and `minMove` controls the minimum price step. Both are derived from `digits`:
- `precision = digits` (e.g., 5 for EURUSD)
- `minMove = 1 / 10^digits` (e.g., 0.00001 for EURUSD)

This also fixes the price scale (y-axis) labels, which were rendering blanks because the default precision (2) didn't match the actual data (5 digits).

**Time scale: `timeVisible: true, secondsVisible: false`**

Lightweight Charts' `timeScale` option supports `timeVisible` which appends HH:mm to the date label when the time is a UNIX timestamp (number). Since we already return UNIX timestamps from the backend, this just enables the flag. `secondsVisible: false` keeps the label clean for trading use.

## Risks / Trade-offs

- **Symbol info fetch failure**: If `getSymbolInfo` fails (network error, unknown symbol), the chart falls back to `digits=5` as a safe default. This is handled in `Layout` with a try/catch.
- **Intraday vs daily timeframes**: `timeVisible` shows HH:mm even on D1/W1/MN1 timeframes, where only the date is meaningful. Lightweight Charts does not offer per-timeframe time formatting. This is acceptable — the time component will just show `00:00` on daily bars.
