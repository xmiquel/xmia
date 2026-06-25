## Context

The Watchlist in `Layout.tsx` hardcodes `DEFAULT_SYMBOLS = ["EURUSD", "GBPUSD", "BTCUSD"]`. There is no backend endpoint to list available symbols — only `GET /api/v1/symbols/{symbol}` for individual lookup. The MT5 Python API provides `symbols_get()` which returns all symbols with metadata, including a `visible` flag indicating whether they appear in the Market Watch.

## Goals / Non-Goals

**Goals:**
- Backend endpoint `GET /api/v1/symbols` returning visible symbol names from MT5
- Frontend fetches this list on mount and displays it in the Watchlist
- Live adapter uses `mt5.symbols_get()` filtering by `visible == True`
- Fake adapter returns a representative set for testing

**Non-Goals:**
- Search/filter across all symbols (visible or not)
- Activating non-visible symbols
- Symbol metadata beyond names (description, group, spread)
- Real-time symbol list updates (polling)

## Decisions

**Return type `list[str]` vs `list[dict]`:** Chose `list[str]` (flat names). YAGNI — we don't need description, group, or other fields yet. Adding object fields later is non-breaking.

**Method name `get_symbols` vs `get_visible_symbols`:** Chose `get_symbols` on the adapter protocol (matches `mt5.symbols_get` naming). The "visible" semantic is a detail of the live implementation.

**No pagination needed:** MT5 typically has a few hundred symbols visible, which is trivially small for a single response.

**Frontend fetch timing:** Fetch on mount (in `useEffect`), same as `fetchRates` and `fetchAccount`. No polling for now.

## Risks / Trade-offs

- **[MT5 symbols_get includes non-visible by default]** → Live adapter filters by `visible == True`. No action needed.
- **[Large venue with thousands of visible symbols]** → Unlikely. Even major brokers show <500 visible symbols. `symbols_get()` returns instantly.
- **[Symbol list doesn't change during session]** → True, but acceptable for v1. We can add polling later if users add/remove symbols from Market Watch.
- **[Fake adapter list diverges from real MT5]** → Acceptable. The fake is for tests and development without MT5.
