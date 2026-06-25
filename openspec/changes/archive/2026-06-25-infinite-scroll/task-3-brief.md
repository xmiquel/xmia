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
