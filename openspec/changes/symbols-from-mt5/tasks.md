# Symbols from MT5 — Implementation Plan

**Goal:** Replace hardcoded `DEFAULT_SYMBOLS` with the list of visible symbols fetched from MT5's Market Watch.

**Architecture:** Backend adds `get_symbols()` to the MT5 adapter protocol, with live implementation calling `mt5.symbols_get()` filtered by `visible == True`. New `GET /api/v1/symbols` endpoint. Frontend fetches on mount and passes to `Watchlist`.

**Tech Stack:** Python (FastAPI, pytest), TypeScript (React, Vitest)

---

### Task 1: Backend — Add `get_symbols` to protocol and adapters

**Files:**
- Modify: `src/mt5/protocol.py`
- Modify: `src/mt5/live.py`
- Modify: `src/mt5/fake.py`
- Modify: `tests/test_protocol.py`

- [x] 1.1 Add `get_symbols` to protocol in `src/mt5/protocol.py` and add `"get_symbols"` to `expected_methods` in `tests/test_protocol.py`
- [x] 1.2 Implement in `LiveMT5Adapter` — call `mt5.symbols_get()` filter by `visible == True`, return `list[str]` of `.name`
- [x] 1.3 Implement in `FakeMT5Adapter` — return `["EURUSD", "GBPUSD", "BTCUSD", "AUDUSD", "USDJPY"]`
- [x] 1.4 Run tests: `uv run pytest tests/test_fake.py tests/test_protocol.py -v`
- [x] 1.5 Commit

---

### Task 2: Backend — Add `GET /api/v1/symbols` endpoint

**Files:**
- Modify: `src/api/services/symbols_service.py`
- Modify: `src/api/routers/symbols.py`
- Modify: `tests/api/test_symbols.py`

- [x] 2.1 Add `get_symbols()` to `SymbolsService` in `symbols_service.py`
- [x] 2.2 Add `GET /api/v1/symbols` route in `symbols_router.py`
- [x] 2.3 Write API tests: happy path (returns list), not-connected returns 503
- [x] 2.4 Run tests: `uv run pytest tests/api/test_symbols.py -v`
- [x] 2.5 Commit

---

### Task 3: Frontend — Add `getSymbols` to API layer

**Files:**
- Modify: `frontend/src/api/symbols.ts`

- [x] 3.1 Add `getSymbols(): Promise<string[]>` calling `GET /api/v1/symbols`
- [x] 3.2 Run typecheck: `cd frontend && npx tsc --noEmit`
- [x] 3.3 Commit

---

### Task 4: Frontend — Wire dynamic symbols into Layout

**Files:**
- Modify: `frontend/src/components/Layout.tsx`
- Modify: `frontend/tests/components/Layout.test.tsx`

- [ ] 4.1 Replace `DEFAULT_SYMBOLS` with `symbols` state and `useEffect` to fetch on mount
- [ ] 4.2 Pass `symbols` to `Watchlist` (component already accepts `symbols` prop)
- [ ] 4.3 Keep `selectedSymbol` defaulting to first symbol from the list (or "EURUSD" as fallback)
- [ ] 4.4 Update Layout tests: mock `getSymbols`, verify it's called on render
- [ ] 4.5 Run frontend tests: `cd frontend && npx vitest run`
- [ ] 4.6 Run typecheck: `cd frontend && npx tsc --noEmit`
- [ ] 4.7 Commit

---

### Task 5: Verify — full test suite

**Files:**
- No file changes — verification only

- [ ] 5.1 Run full backend suite: `uv run pytest tests/ -v`
- [ ] 5.2 Run full frontend suite: `cd frontend && npx vitest run`
- [ ] 5.3 Frontend typecheck: `cd frontend && npx tsc --noEmit`
- [ ] 5.4 Frontend lint: `cd frontend && npx eslint src/`
- [ ] 5.5 Final commit
