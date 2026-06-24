## 1. Layout — fetch digits from symbol API

- [x] 1.1 Add `getSymbolInfo` import to `Layout.tsx`
- [x] 1.2 Add `digits` state (`useState(5)`) and `fetchSymbolInfo` callback
- [x] 1.3 Call `fetchSymbolInfo` when `selectedSymbol` changes (in the rates `useEffect`)
- [x] 1.4 Pass `digits={digits}` prop to `<PriceChart>`
- [x] 1.5 Update `Layout.test.tsx` — mock `getSymbolInfo`, verify `digits` prop passed to PriceChart

## 2. PriceChart — price precision and time scale

- [x] 2.1 Add `digits` to `PriceChart` Props interface
- [x] 2.2 Destructure `digits` from props
- [x] 2.3 Add `priceFormat` to `addCandlestickSeries` with `precision` and `minMove` derived from `digits`
- [x] 2.4 Add `timeVisible: true` and `secondsVisible: false` to `timeScale` options
- [x] 2.5 Update `PriceChart.test.tsx` — pass `digits={5}` in test render

## 3. Verify

- [x] 3.1 Run `npm run test` — all 18 frontend tests pass
- [x] 3.2 Run `npm run build` — no TypeScript or build errors
- [ ] 3.3 Restart frontend dev server if running, verify chart shows correct precision and HH:mm
