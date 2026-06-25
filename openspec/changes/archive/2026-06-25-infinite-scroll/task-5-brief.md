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

Also update imports — add `useRef` and `getRatesBeforeSymbol`:

```typescript
import { useState, useEffect, useCallback, useRef } from "react";
import { getRates, getRatesBeforeSymbol } from "../api/rates";
```

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

Add `handleVisibleRangeChange` with refs to avoid stale closures:

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
      // silent — TradingView-style
    } finally {
      setIsLoadingMore(false);
    }
  },
  [selectedSymbol, timeframe],
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

- [ ] **Step 2: Update Layout tests**

In `frontend/tests/components/Layout.test.tsx`:

Update the rates mock to include `getRatesBeforeSymbol`:

```typescript
vi.mock("../../src/api/rates", () => ({
  getRates: vi.fn().mockResolvedValue([
    { time: 1780272000, open: 1.1, high: 1.11, low: 1.09, close: 1.105, tick_volume: 100, spread: 10, real_volume: 100000 },
  ]),
  getRatesBeforeSymbol: vi.fn().mockResolvedValue([]),
}));
```

Add test for infinite scroll (also add `beforeEach`):

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import Layout from "../../src/components/Layout";

// existing mocks for account, symbols, rates...

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
