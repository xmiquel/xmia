## 1. Backend: Add new fields to rates response

- [x] 1.1 Update `live.py` `get_rates()` to extract `tick_volume` (index 5), `spread` (index 6), and `real_volume` (index 7) from the MT5 rates array
- [x] 1.2 Update `fake.py` `get_rates()` to generate realistic `tick_volume` (int, varying around current volume), `spread` (int, 1–20), and `real_volume` (int, tick_volume * contract_size / 1000)
- [x] 1.3 Update Python tests: `test_live.py` (mock returns extra fields), `test_fake.py` (assert new fields present), `test_contract.py` (contract passes for both adapters)
- [x] 1.4 Run `pytest --runlive` to verify backend still passes

## 2. Frontend: Update data types

- [x] 2.1 Add `tick_volume`, `spread`, `real_volume` fields to the `Candle` interface in `frontend/src/types.ts`
- [x] 2.2 Update `RatesService` or the fetch layer if needed (should pass through automatically)

## 3. Frontend: Create DataWindow component

- [x] 3.1 Create `frontend/src/components/DataWindow.tsx` — HTML overlay component with props: `candle` (Candle | null), `digits`, `position` ({ x, y })
- [x] 3.2 Implement MT5-style layout: dark background (`rgba(0,0,0,0.85)`), white monospace text, label:value two-column rows for Date, Time, Open, High, Low, Close, Volume, Tick Volume, Spread
- [x] 3.3 Implement edge clamping logic: flip to left side if near right edge, flip above if near bottom edge
- [x] 3.4 Create `frontend/src/components/DataWindow.css` with styling (position absolute, transform translate for GPU positioning, compact padding, border radius)

## 4. Frontend: Integrate DataWindow into PriceChart

- [x] 4.1 In `PriceChart.tsx`, subscribe to chart `crosshairMoved` event
- [x] 4.2 Build a `Map<time, Candle>` for O(1) candle lookup on crosshair move
- [x] 4.3 On `crosshairMoved`, find candle by time, pass to DataWindow component
- [x] 4.4 Hide DataWindow when crosshair param is empty (no hover)
- [x] 4.5 Pass `digits` prop through to DataWindow for correct price formatting

## 5. Frontend: Tests

- [x] 5.1 Write unit tests for DataWindow component: renders with candle data, hides when candle is null, shows correct Date/Time/OHLCV/Volume/Spread, clamps position near edges
- [x] 5.2 Write integration tests for PriceChart with DataWindow: crosshair move triggers tooltip, crosshair leave hides tooltip
- [x] 5.3 Run `npm run build` and `npm test` to verify everything compiles and passes

## 6. Manual verification

- [ ] 6.1 Start backend and frontend, verify data window appears on hover with correct values and MT5-style styling
- [ ] 6.2 Verify edge clamping works (move crosshair to right/bottom edges)
