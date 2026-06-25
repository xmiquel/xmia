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

3. Add refs:

```typescript
const visibleRangeCbRef = useRef(onVisibleRangeChange);
```

4. Sync ref when prop changes:

```typescript
useEffect(() => {
  visibleRangeCbRef.current = onVisibleRangeChange;
}, [onVisibleRangeChange]);
```

5. Subscribe to the event in the chart creation `useEffect` (after chart is created, before resize handler):

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
