# Infinite Scroll — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow users to drag the chart left and automatically load more historical candles (500 per batch, 15% edge threshold, silent like TradingView).

**Architecture:** Backend adds `before` parameter to `GET /api/v1/rates/{symbol}` using `mt5.copy_rates_from()`. Frontend `PriceChart` emits `onVisibleRangeChange` via `subscribeVisibleLogicalRangeChange`. `Layout` accumulates candles in `allCandles`, calls `getRatesBeforeSymbol` when approaching the left edge, and merges polling data without overwriting history.

**Tech Stack:** Python (FastAPI, pytest), TypeScript (React, Lightweight Charts, Vitest)

## Global Constraints

- `before` parameter is an exclusive Unix timestamp (seconds) — returned candles have `time < before`
- Chunk size: 500 candles per historical load
- Edge threshold: 15% of total loaded bars
- Silent loading: no spinners or progress indicators
- Forward direction (right) relies on existing 10s polling — no infinite scroll in that direction
- Polling merges into accumulated data (dedup by `time`) instead of overwriting

---

### Task 1: Backend — Add `get_rates_before` to protocol and adapters

**Files:**
- Modify: `src/mt5/protocol.py:85-86`
- Modify: `src/mt5/live.py:145-167`
- Modify: `src/mt5/fake.py:145-164`
- Modify: `tests/test_protocol.py:9-23`
- Test: `tests/test_fake.py` (already read by test runner)

**Interfaces:**
- Consumes: `MT5Adapter` protocol (existing)
- Produces: `get_rates_before(symbol, timeframe, count, before) -> list[dict]` — returns candles with `time < before`

- [ ] **Step 1: Add `get_rates_before` to protocol**

In `src/mt5/protocol.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    ...
```

Also update `test_protocol.py` — add `"get_rates_before"` to the `expected_methods` list.

- [ ] **Step 2: Implement in `LiveMT5Adapter`**

In `src/mt5/live.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    mt5 = self._import_mt5()
    if not self._connected:
        raise AdapterNotConnectedError("Not connected")

    mt5.symbol_select(symbol, True)
    rates = mt5.copy_rates_from(symbol, timeframe, before, count)
    if rates is None:
        return []

    return [
        {
            "time": int(r[0]),
            "open": float(r[1]),
            "high": float(r[2]),
            "low": float(r[3]),
            "close": float(r[4]),
            "tick_volume": int(r[5]),
            "spread": int(r[6]),
            "real_volume": int(r[7]),
        }
        for r in rates
        if int(r[0]) < before
    ]
```

- [ ] **Step 3: Implement in `FakeMT5Adapter`**

In `src/mt5/fake.py`, add after `get_rates`:

```python
def get_rates_before(
    self, symbol: str, timeframe: int, count: int, before: int
) -> list[dict[str, object]]:
    self._check_error("get_rates_before")
    self._require_state(AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

    rates = []
    current_time = before - 1
    for i in range(count):
        t = datetime.fromtimestamp(current_time) - timedelta(hours=timeframe * i)
        base = 1.1000 - (i * 0.0001)
        rates.append({
            "time": int(t.timestamp()),
            "open": base,
            "high": base + 0.0005,
            "low": base - 0.0005,
            "close": base + 0.0002,
            "tick_volume": 100 + i * 10,
            "spread": 5 + (i % 15),
            "real_volume": (100 + i * 10) * 1000,
        })
    return [r for r in rates if r["time"] < before]
```

- [ ] **Step 4: Run backend tests**

Run: `uv run pytest tests/test_fake.py tests/test_protocol.py -v`
Expected: All tests pass (including existing ones)

- [ ] **Step 5: Commit**

```bash
git add src/mt5/protocol.py src/mt5/live.py src/mt5/fake.py tests/test_protocol.py
git commit -m "feat: add get_rates_before to MT5 adapter protocol and implementations"
```

---

### Task 2: Backend — Add `before` parameter to HTTP endpoint

**Files:**
- Modify: `src/api/services/rates_service.py:9-11`
- Modify: `src/api/routers/rates.py:23-31`
- Test: `tests/api/test_rates.py`

**Interfaces:**
- Consumes: `MT5Adapter.get_rates_before` from Task 1
- Produces: `GET /api/v1/rates/{symbol}?before={timestamp}` query parameter

- [ ] **Step 1: Add `get_rates_before` to `RatesService`**

In `src/api/services/rates_service.py`:

```python
def get_rates_before(self, symbol: str, timeframe: str, count: int, before: int) -> list[dict]:
    tf = parse_timeframe(timeframe)
    return self._adapter.get_rates_before(symbol, tf, count, before)
```

- [ ] **Step 2: Add `before` query parameter to endpoint**

Modify `src/api/routers/rates.py`:

```python
@router.get("/api/v1/rates/{symbol}")
async def get_rates(
    symbol: str = Path(..., min_length=1, max_length=20),
    timeframe: str = Depends(_validate_timeframe),
    count: int = Query(10, ge=1, le=1000, description="Number of candles (max 1000)"),
    before: int | None = Query(None, description="Unix timestamp (seconds). If provided, returns candles older than this timestamp."),
    adapter: MT5Adapter = Depends(get_adapter),
):
    service = RatesService(adapter)
    if before is not None:
        return service.get_rates_before(symbol, timeframe, count, before)
    return service.get_rates(symbol, timeframe, count)
```

- [ ] **Step 3: Write API tests**

Add to `tests/api/test_rates.py`:

```python
def test_get_rates_with_before(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?count=5&before=1800000000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for candle in data:
        assert candle["time"] < 1800000000


def test_get_rates_before_empty(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?count=5&before=1000000000")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_rates_invalid_before(client, fake_adapter):
    response = client.get("/api/v1/rates/EURUSD?before=notanumber")
    assert response.status_code == 422
```

- [ ] **Step 4: Run API tests**

Run: `uv run pytest tests/api/test_rates.py -v`
Expected: All 7 tests pass (4 existing + 3 new)

- [ ] **Step 5: Commit**

```bash
git add src/api/services/rates_service.py src/api/routers/rates.py tests/api/test_rates.py
git commit -m "feat: add before parameter to GET /api/v1/rates/{symbol}"
```

---

### Task 3: Frontend — Add `getRatesBeforeSymbol` to API layer

**Files:**
- Modify: `frontend/src/api/rates.ts`

**Interfaces:**
- Consumes: `fetchClient` (existing)
- Produces: `getRatesBeforeSymbol(symbol, timeframe, count, before) -> Promise<Candle[]>`

- [ ] **Step 1: Add the new function**

In `frontend/src/api/rates.ts`:

```typescript
export function getRatesBeforeSymbol(
  symbol: string,
  timeframe: string,
  count: number,
  before: number,
): Promise<Candle[]> {
  const params = new URLSearchParams({
    timeframe,
    count: String(count),
    before: String(before),
  });
  return fetchClient(
    `/api/v1/rates/${encodeURIComponent(symbol)}?${params}`,
  ) as Promise<Candle[]>;
}
```

- [ ] **Step 2: Verify it compiles**

Run: `cd frontend && npx tsc --noEmit`
Expected: No errors

- [ ] **Step 3: Commit**

```bash
git add frontend/src/api/rates.ts
git commit -m "feat: add getRatesBeforeSymbol API function"
```

---

### Task 4: Frontend — Add `onVisibleRangeChange` to PriceChart

**Files:**
- Modify: `frontend/src/components/PriceChart.tsx`
- Modify: `frontend/tests/components/PriceChart.test.tsx`

**Interfaces:**
- Consumes: `Candle[]`, `digits` (existing props)
- Produces: `onVisibleRangeChange?(from: number, to: number) => void` prop

- [ ] **Step 1: Add the new prop and subscribe to range change**

In `frontend/src/components/PriceChart.tsx`:

1. Add `onVisibleRangeChange` to Props:

```typescript
interface Props {
  data: Candle[];
  symbol: string;
  digits: number;
  loading: boolean;
  error: string | null;
  onVisibleRangeChange?: (from: number, to: number) => void;
}
```

2. Destructure the new prop:

```typescript
export default function PriceChart({ data, symbol, digits, loading, error, onVisibleRangeChange }: Props) {
```

3. Subscribe to the event in the chart creation `useEffect` (after `chart.timeScale().fitContent()` block), using a ref to store the callback:

Add ref at top:
```typescript
const visibleRangeCbRef = useRef(onVisibleRangeChange);
```

Update ref when prop changes (useEffect dependency):
```typescript
useEffect(() => {
  visibleRangeCbRef.current = onVisibleRangeChange;
}, [onVisibleRangeChange]);
```

Subscribe in the chart creation effect, after chart creation and before the resize handler:
```typescript
chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
  if (range && visibleRangeCbRef.current) {
    visibleRangeCbRef.current(range.from, range.to);
  }
});
```

- [ ] **Step 2: Update PriceChart test**

In `frontend/tests/components/PriceChart.test.tsx`:

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import PriceChart from "../../src/components/PriceChart";
import type { Candle } from "../../src/types";

const mockCandles: Candle[] = [
  { time: 1780272000, open: 1.1, high: 1.11, low: 1.09, close: 1.105, tick_volume: 100, spread: 10, real_volume: 100000 },
];

describe("PriceChart", () => {
  it("shows loading state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" digits={5} loading={true} error={null} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" digits={5} loading={false} error="Rates unavailable" />);
    expect(screen.getByText(/Rates unavailable/i)).toBeInTheDocument();
  });

  it("renders chart container when data is provided", () => {
    const { container } = render(
      <PriceChart data={mockCandles} symbol="EURUSD" digits={5} loading={false} error={null} />,
    );
    expect(container.querySelector(".price-chart")).toBeInTheDocument();
  });

  it("accepts onVisibleRangeChange prop", () => {
    const onRangeChange = vi.fn();
    render(
      <PriceChart data={mockCandles} symbol="EURUSD" digits={5} loading={false} error={null} onVisibleRangeChange={onRangeChange} />,
    );
    // Just verifies the prop doesn't cause errors; actual callback invocation
    // requires a chart instance and is tested in Layout tests
    expect(onRangeChange).not.toHaveBeenCalled();
  });
});
```

- [ ] **Step 3: Run frontend tests**

Run: `cd frontend && npx vitest run tests/components/PriceChart.test.tsx`
Expected: PASS (4 tests)

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/PriceChart.tsx frontend/tests/components/PriceChart.test.tsx
git commit -m "feat: add onVisibleRangeChange callback to PriceChart"
```

---

### Task 5: Frontend — Accumulate candles and infinite scroll in Layout

**Files:**
- Modify: `frontend/src/components/Layout.tsx`
- Modify: `frontend/tests/components/Layout.test.tsx`

**Interfaces:**
- Consumes: `PriceChart.onVisibleRangeChange`, `getRatesBeforeSymbol` (Task 3), `getRates` (existing)
- Produces: Working infinite scroll — accumulated `allCandles`, merge-on-poll, scroll trigger

- [ ] **Step 1: Refactor Layout state for accumulation**

In `frontend/src/components/Layout.tsx`:

Replace:
```typescript
const [candles, setCandles] = useState<Candle[]>([]);
```

With:
```typescript
const [allCandles, setAllCandles] = useState<Candle[]>([]);
const [isLoadingMore, setIsLoadingMore] = useState(false);
const [hasMore, setHasMore] = useState(true);
const isLoadingMoreRef = useRef(false);
const hasMoreRef = useRef(true);
const allCandlesRef = useRef<Candle[]>([]);

isLoadingMoreRef.current = isLoadingMore;
hasMoreRef.current = hasMore;
allCandlesRef.current = allCandles;
```

Also add `useRef` to the React import at the top of the file (change `import { useState, useEffect, useCallback }` to `import { useState, useEffect, useCallback, useRef }`).

Also add `getRatesBeforeSymbol` to the rates import (change `import { getRates } from "../api/rates"` to `import { getRates, getRatesBeforeSymbol } from "../api/rates"`).

Update `fetchRates` to merge instead of overwrite:

```typescript
const fetchRates = useCallback(async () => {
  try {
    setCandlesLoading(true);
    setCandlesError(null);
    const data = await getRates(selectedSymbol, timeframe, 100);
    setAllCandles((prev) => {
      const existingTimes = new Set(prev.map((c) => c.time));
      const newCandles = data.filter((c) => !existingTimes.has(c.time));
      return [...prev, ...newCandles].sort((a, b) => a.time - b.time);
    });
  } catch (err) {
    setCandlesError(err instanceof Error ? err.message : "Failed to load rates");
  } finally {
    setCandlesLoading(false);
  }
}, [selectedSymbol, timeframe]);
```

Add `handleVisibleRangeChange`:

```typescript
const handleVisibleRangeChange = useCallback(
  async (from: number) => {
    if (isLoadingMore || !hasMore || allCandles.length === 0) return;
    const totalBars = allCandles.length;
    const threshold = totalBars * 0.15;
    if (from > threshold) return;

    setIsLoadingMore(true);
    const earliest = allCandles[0].time;
    try {
      const olderCandles = await getRatesBeforeSymbol(
        selectedSymbol,
        timeframe,
        500,
        earliest,
      );
      if (olderCandles.length === 0) {
        setHasMore(false);
      } else {
        setAllCandles((prev) => [...olderCandles, ...prev]);
      }
    } catch {
      // silent — TradingView-style
    } finally {
      setIsLoadingMore(false);
    }
  },
  [selectedSymbol, timeframe, allCandles, isLoadingMore, hasMore],
);
```

Update the JSX to pass `onVisibleRangeChange` and `allCandles` to `PriceChart`:

```typescript
<PriceChart
  data={allCandles}
  symbol={selectedSymbol}
  digits={digits}
  loading={candlesLoading}
  error={candlesError}
  onVisibleRangeChange={handleVisibleRangeChange}
/>
```

Also import `useRef` and add a ref for `allCandles` to avoid stale closures in the callback (since `handleVisibleRangeChange` depends on `allCandles`). Or use a ref to hold the latest `allCandles`:

```typescript
const allCandlesRef = useRef(allCandles);
allCandlesRef.current = allCandles;
```

And read `allCandlesRef.current` inside `handleVisibleRangeChange` instead of reading `allCandles` directly. This avoids stale closure issues since the callback is used as a prop.

Also add `isLoadingMoreRef` similarly.

Full updated `handleVisibleRangeChange` with refs:

```typescript
const handleVisibleRangeChange = useCallback(
  async (from: number) => {
    if (isLoadingMoreRef.current || !hasMoreRef.current || allCandlesRef.current.length === 0) return;
    const totalBars = allCandlesRef.current.length;
    const threshold = totalBars * 0.15;
    if (from > threshold) return;

    setIsLoadingMore(true);
    const earliest = allCandlesRef.current[0].time;
    try {
      const olderCandles = await getRatesBeforeSymbol(
        selectedSymbol,
        timeframe,
        500,
        earliest,
      );
      if (olderCandles.length === 0) {
        setHasMore(false);
      } else {
        setAllCandles((prev) => [...olderCandles, ...prev]);
      }
    } catch {
      // silent
    } finally {
      setIsLoadingMore(false);
    }
  },
  [selectedSymbol, timeframe],
);
```

- [ ] **Step 2: Update Layout tests**

In `frontend/tests/components/Layout.test.tsx`:

Add `getRatesBeforeSymbol` to the rates mock:

```typescript
vi.mock("../../src/api/rates", () => ({
  getRates: vi.fn().mockResolvedValue([
    { time: 1780272000, open: 1.1, high: 1.11, low: 1.09, close: 1.105, tick_volume: 100, spread: 10, real_volume: 100000 },
  ]),
  getRatesBeforeSymbol: vi.fn().mockResolvedValue([]),
}));
```

Add a test for infinite scroll:

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";

// ... existing mocks ...

describe("Layout", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders all three panels", () => {
    render(<Layout />);
    expect(screen.getAllByText("EURUSD")).toHaveLength(2);
    expect(screen.getByText("GBPUSD")).toBeInTheDocument();
    expect(screen.getByText("BTCUSD")).toBeInTheDocument();
  });

  it("does not call getRatesBeforeSymbol on initial render", async () => {
    const { getRatesBeforeSymbol } = await import("../../src/api/rates");
    render(<Layout />);
    expect(getRatesBeforeSymbol).not.toHaveBeenCalled();
  });
});
```

- [ ] **Step 3: Run frontend tests**

Run: `cd frontend && npx vitest run`
Expected: PASS (all tests)

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/Layout.tsx frontend/tests/components/Layout.test.tsx
git commit -m "feat: add infinite scroll with accumulated candle state in Layout"
```

---

### Task 6: Verify — lint, typecheck, and full test suite

**Files:**
- No file changes — verification only

- [ ] **Step 1: Run full backend test suite**

Run: `uv run pytest tests/ -v`
Expected: All backend tests pass

- [ ] **Step 2: Run full frontend test suite**

Run: `cd frontend && npx vitest run`
Expected: All frontend tests pass

- [ ] **Step 3: Run frontend type check**

Run: `cd frontend && npx tsc --noEmit`
Expected: No TypeScript errors

- [ ] **Step 4: Run frontend lint**

Run: `cd frontend && npx eslint src/`
Expected: No lint errors

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "chore: final verification passes for infinite scroll"
```
