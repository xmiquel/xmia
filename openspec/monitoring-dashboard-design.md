# Monitoring Dashboard — Design

## Stack

- **Frontend**: React + TypeScript + Vite
- **Charts**: Lightweight Charts (TradingView)
- **Testing**: Vitest + @testing-library/react
- **Linting**: ESLint + eslint-plugin-react + eslint-plugin-react-hooks + eslint-plugin-security
- **Backend**: FastAPI (existing `api-core`)

---

## Architecture

```
mi-api/
├── src/                          # Backend (existing)
├── frontend/                     # New directory
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   │   ├── client.ts         # Fetch wrapper with X-API-Key header
│   │   │   ├── account.ts        # GET /api/v1/account
│   │   │   ├── symbols.ts        # GET /api/v1/symbols/{symbol}
│   │   │   └── rates.ts          # GET /api/v1/rates/{symbol}
│   │   ├── components/
│   │   │   ├── Layout.tsx        # 3-column CSS Grid
│   │   │   ├── Watchlist.tsx
│   │   │   ├── PriceChart.tsx    # Lightweight Charts
│   │   │   ├── AccountSummary.tsx
│   │   │   └── TimeframeSelector.tsx
│   │   └── types.ts
│   └── tests/
├── pyproject.toml
└── openspec/
```

---

## Layout

3-column CSS Grid:

```
┌─────────────┬──────────────────────┬─────────────┐
│  Watchlist  │                      │   Account   │
│  ─────────  │    Price Chart       │   Summary   │
│  EURUSD     │    (Lightweight      │  ─────────  │
│  GBPUSD     │     Charts)          │  Balance    │
│  BTCUSD     │                      │  Equity     │
│             │                      │  Margin     │
│             │                      │  Free Mg    │
│             │                      │  Mg Level   │
│             │                      │             │
│  [Timeframe Selector: M1 M5 H1 D1] │             │
└─────────────┴──────────────────────┴─────────────┘
```

---

## Data Flow

1. App mounts → `useEffect` fetches `GET /api/v1/account` → populates `AccountSummary`
2. Default symbol is EURUSD → `GET /api/v1/rates/EURUSD?timeframe=PERIOD_H1&count=100`
3. User clicks symbol in `Watchlist` → refetch chart rates for selected symbol
4. `TimeframeSelector` changes timeframe → refetch chart rates
5. Polling every 10s: refetch account info and latest rates
6. Proxy in `vite.config.ts`: `/api` → `localhost:8000`

---

## States per Component

Each data-fetching component handles:
- **Loading**: spinner or skeleton
- **Error**: message with retry button
- **Empty**: no data placeholder (e.g., no rates yet)
- **Data**: normal render

---

## Testing

- **Vitest** + **@testing-library/react**
- Test components render loading, error, and data states
- Mock api layer to avoid real HTTP calls
- No E2E for MVP (Playwright deferred)

---

## Non-Goals (v1)

- No routing (single `/dashboard` page)
- No WebSockets (polling only)
- No real-time updates (polling every 10s)
- No order/position management
- No dark/light theme toggle
- No Docker for frontend (runs on host via Vite dev server)
