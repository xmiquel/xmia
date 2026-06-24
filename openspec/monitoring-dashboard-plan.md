# Monitoring Dashboard — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a React + Vite dashboard with watchlist, OHLCV price chart (Lightweight Charts), and account summary panel.

**Architecture:** Single-page app with 3-column CSS Grid layout. Polling every 10s for data refresh. Vite proxies `/api` to FastAPI backend (`localhost:8000`). No routing (single `/dashboard` view).

**Tech Stack:** React 19, TypeScript, Vite 6, Lightweight Charts 4, Vitest, @testing-library/react, ESLint

## Global Constraints

- Python backend runs on Windows host; frontend runs on host via Vite dev server
- API Key auth via `X-API-Key` header (optional — dev mode disabled when unset)
- Backend endpoints: `GET /api/v1/account`, `GET /api/v1/symbols/{symbol}`, `GET /api/v1/rates/{symbol}?timeframe=&count=`
- Timeframes: PERIOD_M1, M3, M5, M6, M12, M15, M24, M30, H1, H4, D1, W1, MN1
- Default timeframe: PERIOD_H1, default count: 100
- Max count: 1000

---

## File Structure

```
frontend/
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── eslint.config.js
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── types.ts
│   ├── api/
│   │   ├── client.ts
│   │   ├── account.ts
│   │   ├── symbols.ts
│   │   └── rates.ts
│   └── components/
│       ├── Layout.tsx
│       ├── Layout.css
│       ├── Watchlist.tsx
│       ├── Watchlist.css
│       ├── PriceChart.tsx
│       ├── PriceChart.css
│       ├── AccountSummary.tsx
│       ├── AccountSummary.css
│       ├── TimeframeSelector.tsx
│       └── TimeframeSelector.css
└── tests/
    ├── setup.ts
    ├── api/
    │   └── client.test.ts
    └── components/
        ├── AccountSummary.test.tsx
        ├── Watchlist.test.tsx
        ├── TimeframeSelector.test.tsx
        ├── PriceChart.test.tsx
        ├── Layout.test.tsx
        └── App.test.tsx
```

---

### Task 1: Project Scaffolding

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tsconfig.node.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/eslint.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/tests/setup.ts`

**Interfaces:**
- Consumes: nothing
- Produces: working Vite dev server at `localhost:5173`, Vitest runner configured

- [ ] **Step 1: Create `frontend/package.json`**

```json
{
  "name": "mi-api-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint src/"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "lightweight-charts": "^4.2.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.0.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.4.0",
    "eslint": "^9.0.0",
    "eslint-plugin-react": "^7.37.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-security": "^3.0.0",
    "globals": "^16.0.0",
    "jsdom": "^26.0.0",
    "typescript": "~5.7.0",
    "typescript-eslint": "^8.0.0",
    "vite": "^6.2.0",
    "vitest": "^3.1.0"
  }
}
```

- [ ] **Step 2: Create `frontend/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true
  },
  "include": ["src", "tests"]
}
```

- [ ] **Step 3: Create `frontend/tsconfig.node.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 4: Create `frontend/vite.config.ts`**

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./tests/setup.ts",
  },
});
```

- [ ] **Step 5: Create `frontend/eslint.config.js`**

```js
import js from "@eslint/js";
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import security from "eslint-plugin-security";
import globals from "globals";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.strict,
  reactPlugin.configs.flat["jsx-runtime"],
  {
    plugins: {
      "react-hooks": reactHooks,
      security,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "security/detect-object-injection": "warn",
    },
    languageOptions: {
      globals: { ...globals.browser, ...globals.es2020 },
    },
    settings: {
      react: { version: "detect" },
    },
  },
];
```

- [ ] **Step 6: Create `frontend/index.html`**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mi-api Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 7: Create `frontend/src/main.tsx`**

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./App.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

- [ ] **Step 8: Create `frontend/tests/setup.ts`**

```ts
import "@testing-library/jest-dom";
```

- [ ] **Step 9: Install dependencies and verify**

```bash
cd frontend
npm install
```

- [ ] **Step 10: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold Vite + React + TypeScript frontend"
```

---

### Task 2: Types + API Layer

**Files:**
- Create: `frontend/src/types.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/account.ts`
- Create: `frontend/src/api/symbols.ts`
- Create: `frontend/src/api/rates.ts`
- Create: `frontend/tests/api/client.test.ts`

**Interfaces:**
- Consumes: nothing
- Produces: `AccountInfo`, `SymbolInfo`, `Candle` types; `fetchClient`, `getAccountInfo`, `getSymbolInfo`, `getRates` functions

- [ ] **Step 1: Create `frontend/src/types.ts`**

```ts
export interface AccountInfo {
  balance: number;
  equity: number;
  margin: number;
  free_margin: number;
  margin_level: number;
  currency: string;
  name: string;
  server: string;
  leverage: number;
}

export interface SymbolInfo {
  symbol: string;
  digits: number;
  spread: number;
  margin_currency: string;
  contract_size: number;
}

export interface Candle {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

- [ ] **Step 2: Create `frontend/src/api/client.ts`**

```ts
const API_KEY = import.meta.env.VITE_API_KEY;

export async function fetchClient(path: string): Promise<unknown> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (API_KEY) {
    headers["X-API-Key"] = API_KEY;
  }
  const res = await fetch(path, { headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}
```

- [ ] **Step 3: Create `frontend/src/api/account.ts`**

```ts
import { fetchClient } from "./client";
import type { AccountInfo } from "../types";

export function getAccountInfo(): Promise<AccountInfo> {
  return fetchClient("/api/v1/account") as Promise<AccountInfo>;
}
```

- [ ] **Step 4: Create `frontend/src/api/symbols.ts`**

```ts
import { fetchClient } from "./client";
import type { SymbolInfo } from "../types";

export function getSymbolInfo(symbol: string): Promise<SymbolInfo> {
  return fetchClient(`/api/v1/symbols/${encodeURIComponent(symbol)}`) as Promise<SymbolInfo>;
}
```

- [ ] **Step 5: Create `frontend/src/api/rates.ts`**

```ts
import { fetchClient } from "./client";
import type { Candle } from "../types";

export function getRates(
  symbol: string,
  timeframe = "PERIOD_H1",
  count = 100,
): Promise<Candle[]> {
  const params = new URLSearchParams({ timeframe, count: String(count) });
  return fetchClient(
    `/api/v1/rates/${encodeURIComponent(symbol)}?${params}`,
  ) as Promise<Candle[]>;
}
```

- [ ] **Step 6: Write test for `fetchClient`**

Create `frontend/tests/api/client.test.ts`:

```ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchClient } from "../../src/api/client";

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("fetchClient", () => {
  it("includes X-API-Key header when VITE_API_KEY is set", async () => {
    vi.stubEnv("VITE_API_KEY", "sk-test123");
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: "ok" }),
    });
    await fetchClient("/health");
    expect(fetch).toHaveBeenCalledWith("/health", {
      headers: expect.objectContaining({ "X-API-Key": "sk-test123" }),
    });
    vi.unstubAllEnvs();
  });

  it("omits X-API-Key header when VITE_API_KEY is not set", async () => {
    vi.stubEnv("VITE_API_KEY", "");
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: "ok" }),
    });
    await fetchClient("/health");
    const call = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(call[1].headers["X-API-Key"]).toBeUndefined();
    vi.unstubAllEnvs();
  });

  it("throws with detail on non-ok response", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: "Invalid API Key" }),
    });
    await expect(fetchClient("/api/v1/account")).rejects.toThrow("Invalid API Key");
  });

  it("throws with HTTP status when no detail in body", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.reject(new Error("no json")),
    });
    await expect(fetchClient("/error")).rejects.toThrow("HTTP 500");
  });
});
```

- [ ] **Step 7: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/api/client.test.ts`
Expected: FAIL (no source file yet)

- [ ] **Step 8: Create source files (steps 1-5 above)**

- [ ] **Step 9: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/api/client.test.ts`
Expected: PASS (4 tests)

- [ ] **Step 10: Commit**

```bash
git add frontend/src/types.ts frontend/src/api/ frontend/tests/api/
git commit -m "feat: add API layer with types and fetch client"
```

---

### Task 3: AccountSummary Component

**Files:**
- Create: `frontend/src/components/AccountSummary.tsx`
- Create: `frontend/src/components/AccountSummary.css`
- Create: `frontend/tests/components/AccountSummary.test.tsx`

**Interfaces:**
- Consumes: `AccountInfo` type from types.ts
- Produces: `<AccountSummary account={AccountInfo | null} loading={boolean} error={string | null} />`

- [ ] **Step 1: Write test**

Create `frontend/tests/components/AccountSummary.test.tsx`:

```tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import AccountSummary from "../../src/components/AccountSummary";
import type { AccountInfo } from "../../src/types";

const mockAccount: AccountInfo = {
  balance: 10000,
  equity: 9500,
  margin: 500,
  free_margin: 9000,
  margin_level: 1900,
  currency: "USD",
  name: "Demo",
  server: "MetaQuotes-Demo",
  leverage: 100,
};

describe("AccountSummary", () => {
  it("shows loading state", () => {
    render(<AccountSummary account={null} loading={true} error={null} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(<AccountSummary account={null} loading={false} error="Connection failed" />);
    expect(screen.getByText(/Connection failed/i)).toBeInTheDocument();
  });

  it("renders account fields when data is provided", () => {
    render(<AccountSummary account={mockAccount} loading={false} error={null} />);
    expect(screen.getByText("$10,000.00")).toBeInTheDocument();
    expect(screen.getByText("$9,500.00")).toBeInTheDocument();
    expect(screen.getByText("$500.00")).toBeInTheDocument();
    expect(screen.getByText("$9,000.00")).toBeInTheDocument();
    expect(screen.getByText("1,900.00%")).toBeInTheDocument();
    expect(screen.getByText("USD")).toBeInTheDocument();
    expect(screen.getByText("100")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/components/AccountSummary.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/components/AccountSummary.css`**

```css
.account-summary {
  padding: 16px;
  border-left: 1px solid #e0e0e0;
  min-width: 220px;
}
.account-summary h2 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #333;
}
.account-summary .field {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}
.account-summary .field-label {
  color: #666;
}
.account-summary .field-value {
  font-weight: 600;
  color: #222;
}
.account-summary .error {
  color: #d32f2f;
  font-size: 13px;
}
.account-summary .loading {
  color: #666;
  font-size: 13px;
}
```

- [ ] **Step 4: Create `frontend/src/components/AccountSummary.tsx`**

```tsx
import type { AccountInfo } from "../types";
import "./AccountSummary.css";

interface Props {
  account: AccountInfo | null;
  loading: boolean;
  error: string | null;
}

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
  }).format(value);
}

function formatPercent(value: number): string {
  return `${value.toLocaleString("en-US", { minimumFractionDigits: 2 })}%`;
}

export default function AccountSummary({ account, loading, error }: Props) {
  if (loading) return <div className="account-summary"><div className="loading">Loading account...</div></div>;
  if (error) return <div className="account-summary"><div className="error">{error}</div></div>;
  if (!account) return <div className="account-summary"><div className="loading">No account data</div></div>;

  return (
    <div className="account-summary">
      <h2>Account</h2>
      <div className="field">
        <span className="field-label">Balance</span>
        <span className="field-value">{formatCurrency(account.balance, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Equity</span>
        <span className="field-value">{formatCurrency(account.equity, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Margin</span>
        <span className="field-value">{formatCurrency(account.margin, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Free Margin</span>
        <span className="field-value">{formatCurrency(account.free_margin, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Margin Level</span>
        <span className="field-value">{formatPercent(account.margin_level)}</span>
      </div>
      <div className="field">
        <span className="field-label">Currency</span>
        <span className="field-value">{account.currency}</span>
      </div>
      <div className="field">
        <span className="field-label">Leverage</span>
        <span className="field-value">{account.leverage}</span>
      </div>
    </div>
  );
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/components/AccountSummary.test.tsx`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/AccountSummary.tsx frontend/src/components/AccountSummary.css frontend/tests/components/AccountSummary.test.tsx
git commit -m "feat: add AccountSummary component"
```

---

### Task 4: TimeframeSelector Component

**Files:**
- Create: `frontend/src/components/TimeframeSelector.tsx`
- Create: `frontend/src/components/TimeframeSelector.css`
- Create: `frontend/tests/components/TimeframeSelector.test.tsx`

**Interfaces:**
- Consumes: nothing
- Produces: `<TimeframeSelector value={string} onChange={(tf: string) => void} />`

- [ ] **Step 1: Write test**

Create `frontend/tests/components/TimeframeSelector.test.tsx`:

```tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TimeframeSelector from "../../src/components/TimeframeSelector";

describe("TimeframeSelector", () => {
  it("renders all timeframe buttons", () => {
    render(<TimeframeSelector value="PERIOD_H1" onChange={() => {}} />);
    expect(screen.getByText("M1")).toBeInTheDocument();
    expect(screen.getByText("M5")).toBeInTheDocument();
    expect(screen.getByText("H1")).toBeInTheDocument();
    expect(screen.getByText("H4")).toBeInTheDocument();
    expect(screen.getByText("D1")).toBeInTheDocument();
  });

  it("highlights the active timeframe", () => {
    render(<TimeframeSelector value="PERIOD_H1" onChange={() => {}} />);
    expect(screen.getByText("H1")).toHaveClass("active");
  });

  it("calls onChange with the timeframe constant when clicked", () => {
    const onChange = vi.fn();
    render(<TimeframeSelector value="PERIOD_H1" onChange={onChange} />);
    fireEvent.click(screen.getByText("M5"));
    expect(onChange).toHaveBeenCalledWith("PERIOD_M5");
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/components/TimeframeSelector.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/components/TimeframeSelector.css`**

```css
.timeframe-selector {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}
.timeframe-selector button {
  padding: 4px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 12px;
  color: #333;
}
.timeframe-selector button.active {
  background: #1976d2;
  color: #fff;
  border-color: #1976d2;
}
.timeframe-selector button:hover:not(.active) {
  background: #e3f2fd;
}
```

- [ ] **Step 4: Create `frontend/src/components/TimeframeSelector.tsx`**

```tsx
import "./TimeframeSelector.css";

const TIMEFRAMES = [
  { label: "M1", value: "PERIOD_M1" },
  { label: "M5", value: "PERIOD_M5" },
  { label: "M15", value: "PERIOD_M15" },
  { label: "M30", value: "PERIOD_M30" },
  { label: "H1", value: "PERIOD_H1" },
  { label: "H4", value: "PERIOD_H4" },
  { label: "D1", value: "PERIOD_D1" },
  { label: "W1", value: "PERIOD_W1" },
  { label: "MN1", value: "PERIOD_MN1" },
];

interface Props {
  value: string;
  onChange: (timeframe: string) => void;
}

export default function TimeframeSelector({ value, onChange }: Props) {
  return (
    <div className="timeframe-selector">
      {TIMEFRAMES.map((tf) => (
        <button
          key={tf.value}
          className={value === tf.value ? "active" : ""}
          onClick={() => onChange(tf.value)}
        >
          {tf.label}
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/components/TimeframeSelector.test.tsx`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/TimeframeSelector.tsx frontend/src/components/TimeframeSelector.css frontend/tests/components/TimeframeSelector.test.tsx
git commit -m "feat: add TimeframeSelector component"
```

---

### Task 5: Watchlist Component

**Files:**
- Create: `frontend/src/components/Watchlist.tsx`
- Create: `frontend/src/components/Watchlist.css`
- Create: `frontend/tests/components/Watchlist.test.tsx`

**Interfaces:**
- Consumes: nothing
- Produces: `<Watchlist symbols={string[]} selected={string} onSelect={(symbol: string) => void} />`

- [ ] **Step 1: Write test**

Create `frontend/tests/components/Watchlist.test.tsx`:

```tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Watchlist from "../../src/components/Watchlist";

const SYMBOLS = ["EURUSD", "GBPUSD", "BTCUSD"];

describe("Watchlist", () => {
  it("renders all symbols", () => {
    render(<Watchlist symbols={SYMBOLS} selected="EURUSD" onSelect={() => {}} />);
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("GBPUSD")).toBeInTheDocument();
    expect(screen.getByText("BTCUSD")).toBeInTheDocument();
  });

  it("highlights selected symbol", () => {
    render(<Watchlist symbols={SYMBOLS} selected="GBPUSD" onSelect={() => {}} />);
    expect(screen.getByText("GBPUSD")).toHaveClass("selected");
  });

  it("calls onSelect when a symbol is clicked", () => {
    const onSelect = vi.fn();
    render(<Watchlist symbols={SYMBOLS} selected="EURUSD" onSelect={onSelect} />);
    fireEvent.click(screen.getByText("BTCUSD"));
    expect(onSelect).toHaveBeenCalledWith("BTCUSD");
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/components/Watchlist.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/components/Watchlist.css`**

```css
.watchlist {
  padding: 16px;
  border-right: 1px solid #e0e0e0;
  min-width: 140px;
}
.watchlist h2 {
  margin: 0 0 12px;
  font-size: 16px;
  color: #333;
}
.watchlist ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.watchlist li {
  padding: 8px 10px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 13px;
  color: #333;
}
.watchlist li:hover {
  background: #e3f2fd;
}
.watchlist li.selected {
  background: #1976d2;
  color: #fff;
}
```

- [ ] **Step 4: Create `frontend/src/components/Watchlist.tsx`**

```tsx
import "./Watchlist.css";

interface Props {
  symbols: string[];
  selected: string;
  onSelect: (symbol: string) => void;
}

export default function Watchlist({ symbols, selected, onSelect }: Props) {
  return (
    <div className="watchlist">
      <h2>Symbols</h2>
      <ul>
        {symbols.map((s) => (
          <li
            key={s}
            className={s === selected ? "selected" : ""}
            onClick={() => onSelect(s)}
          >
            {s}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/components/Watchlist.test.tsx`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/Watchlist.tsx frontend/src/components/Watchlist.css frontend/tests/components/Watchlist.test.tsx
git commit -m "feat: add Watchlist component"
```

---

### Task 6: PriceChart Component (Lightweight Charts)

**Files:**
- Create: `frontend/src/components/PriceChart.tsx`
- Create: `frontend/src/components/PriceChart.css`
- Create: `frontend/tests/components/PriceChart.test.tsx`

**Interfaces:**
- Consumes: `Candle` type from types.ts
- Produces: `<PriceChart data={Candle[]} symbol={string} loading={boolean} error={string | null} />`

- [ ] **Step 1: Write test**

Create `frontend/tests/components/PriceChart.test.tsx`:

```tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import PriceChart from "../../src/components/PriceChart";
import type { Candle } from "../../src/types";

const mockCandles: Candle[] = [
  { time: "2026-06-18T10:00:00", open: 1.1, high: 1.11, low: 1.09, close: 1.105, volume: 100 },
];

describe("PriceChart", () => {
  it("shows loading state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" loading={true} error={null} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" loading={false} error="Rates unavailable" />);
    expect(screen.getByText(/Rates unavailable/i)).toBeInTheDocument();
  });

  it("renders chart container when data is provided", () => {
    const { container } = render(
      <PriceChart data={mockCandles} symbol="EURUSD" loading={false} error={null} />,
    );
    expect(container.querySelector(".price-chart")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/components/PriceChart.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/components/PriceChart.css`**

```css
.price-chart {
  flex: 1;
  padding: 16px;
  min-width: 0;
}
.price-chart h2 {
  margin: 0 0 12px;
  font-size: 16px;
  color: #333;
}
.price-chart .chart-container {
  width: 100%;
  height: 400px;
}
.price-chart .loading,
.price-chart .error {
  color: #666;
  font-size: 13px;
  padding: 20px;
}
.price-chart .error {
  color: #d32f2f;
}
```

- [ ] **Step 4: Create `frontend/src/components/PriceChart.tsx`**

```tsx
import { useEffect, useRef } from "react";
import { createChart, ColorType } from "lightweight-charts";
import type { Candle } from "../types";
import "./PriceChart.css";

interface Props {
  data: Candle[];
  symbol: string;
  loading: boolean;
  error: string | null;
}

export default function PriceChart({ data, symbol, loading, error }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { type: ColorType.Solid, color: "#ffffff" },
        textColor: "#333",
      },
      grid: {
        vertLines: { color: "#f0f0f0" },
        horzLines: { color: "#f0f0f0" },
      },
      crosshair: {
        mode: 0,
      },
      timeScale: {
        borderColor: "#e0e0e0",
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderDownColor: "#ef5350",
      borderUpColor: "#26a69a",
      wickDownColor: "#ef5350",
      wickUpColor: "#26a69a",
    });

    candleSeries.setData(
      data.map((c) => ({
        time: c.time,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      })),
    );

    chart.timeScale().fitContent();

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [data]);

  if (loading) return <div className="price-chart"><div className="loading">Loading chart...</div></div>;
  if (error) return <div className="price-chart"><div className="error">{error}</div></div>;

  return (
    <div className="price-chart">
      <h2>{symbol}</h2>
      <div className="chart-container" ref={chartContainerRef} />
    </div>
  );
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/components/PriceChart.test.tsx`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/PriceChart.tsx frontend/src/components/PriceChart.css frontend/tests/components/PriceChart.test.tsx
git commit -m "feat: add PriceChart component with Lightweight Charts"
```

---

### Task 7: Layout Component

**Files:**
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/Layout.css`
- Create: `frontend/tests/components/Layout.test.tsx`

**Interfaces:**
- Consumes: `Watchlist`, `PriceChart`, `TimeframeSelector`, `AccountSummary` components
- Produces: `<Layout />` with 3-column grid + timeframe selector at bottom of center column

- [ ] **Step 1: Write test**

Create `frontend/tests/components/Layout.test.tsx`:

```tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Layout from "../../src/components/Layout";

describe("Layout", () => {
  it("renders all three panels", () => {
    render(<Layout />);
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("GBPUSD")).toBeInTheDocument();
    expect(screen.getByText("BTCUSD")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/components/Layout.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/components/Layout.css`**

```css
.dashboard-layout {
  display: grid;
  grid-template-columns: 140px 1fr 220px;
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
```

- [ ] **Step 4: Create `frontend/src/components/Layout.tsx`**

```tsx
import { useState, useEffect, useCallback } from "react";
import Watchlist from "./Watchlist";
import PriceChart from "./PriceChart";
import AccountSummary from "./AccountSummary";
import TimeframeSelector from "./TimeframeSelector";
import { getAccountInfo } from "../api/account";
import { getRates } from "../api/rates";
import type { AccountInfo, Candle } from "../types";
import "./Layout.css";

const DEFAULT_SYMBOLS = ["EURUSD", "GBPUSD", "BTCUSD"];
const POLL_INTERVAL = 10_000;

export default function Layout() {
  const [selectedSymbol, setSelectedSymbol] = useState("EURUSD");
  const [timeframe, setTimeframe] = useState("PERIOD_H1");

  const [account, setAccount] = useState<AccountInfo | null>(null);
  const [accountLoading, setAccountLoading] = useState(true);
  const [accountError, setAccountError] = useState<string | null>(null);

  const [candles, setCandles] = useState<Candle[]>([]);
  const [candlesLoading, setCandlesLoading] = useState(true);
  const [candlesError, setCandlesError] = useState<string | null>(null);

  const fetchAccount = useCallback(async () => {
    try {
      setAccountLoading(true);
      setAccountError(null);
      const data = await getAccountInfo();
      setAccount(data);
    } catch (err) {
      setAccountError(err instanceof Error ? err.message : "Failed to load account");
    } finally {
      setAccountLoading(false);
    }
  }, []);

  const fetchRates = useCallback(async () => {
    try {
      setCandlesLoading(true);
      setCandlesError(null);
      const data = await getRates(selectedSymbol, timeframe, 100);
      setCandles(data);
    } catch (err) {
      setCandlesError(err instanceof Error ? err.message : "Failed to load rates");
    } finally {
      setCandlesLoading(false);
    }
  }, [selectedSymbol, timeframe]);

  useEffect(() => {
    fetchAccount();
    const interval = setInterval(fetchAccount, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchAccount]);

  useEffect(() => {
    fetchRates();
    const interval = setInterval(fetchRates, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchRates]);

  return (
    <div className="dashboard-layout">
      <Watchlist
        symbols={DEFAULT_SYMBOLS}
        selected={selectedSymbol}
        onSelect={setSelectedSymbol}
      />
      <div>
        <PriceChart
          data={candles}
          symbol={selectedSymbol}
          loading={candlesLoading}
          error={candlesError}
        />
        <TimeframeSelector value={timeframe} onChange={setTimeframe} />
      </div>
      <AccountSummary
        account={account}
        loading={accountLoading}
        error={accountError}
      />
    </div>
  );
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/components/Layout.test.tsx`
Expected: PASS (1 test)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/Layout.tsx frontend/src/components/Layout.css frontend/tests/components/Layout.test.tsx
git commit -m "feat: add dashboard Layout with 3-column grid and data fetching"
```

---

### Task 8: App Integration + App.css

**Files:**
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/App.css`
- Create: `frontend/tests/App.test.tsx`

- [ ] **Step 1: Write test**

Create `frontend/tests/App.test.tsx`:

```tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../src/App";

describe("App", () => {
  it("renders the dashboard layout", () => {
    render(<App />);
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("Account")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd frontend && npx vitest run tests/App.test.tsx`
Expected: FAIL

- [ ] **Step 3: Create `frontend/src/App.css`**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  height: 100%;
  width: 100%;
}
```

- [ ] **Step 4: Create `frontend/src/App.tsx`**

```tsx
import Layout from "./components/Layout";

export default function App() {
  return <Layout />;
}
```

- [ ] **Step 5: Run test to verify pass**

Run: `cd frontend && npx vitest run tests/App.test.tsx`
Expected: PASS (1 test)

- [ ] **Step 6: Run full test suite**

```bash
cd frontend && npx vitest run
```

Expected: All 18 tests pass

- [ ] **Step 7: Commit**

```bash
git add frontend/src/App.tsx frontend/src/App.css frontend/tests/App.test.tsx
git commit -m "feat: integrate App component with Layout"
```

---

### Task 9: Verify lint + full suite

- [ ] **Step 1: Run ESLint**

```bash
cd frontend && npx eslint src/
```
Expected: No errors

- [ ] **Step 2: Run type check**

```bash
cd frontend && npx tsc --noEmit
```
Expected: No errors

- [ ] **Step 3: Run all tests**

```bash
cd frontend && npx vitest run
```
Expected: All tests pass

- [ ] **Step 4: Run backend tests to ensure no regressions**

```bash
cd .. && uv run pytest tests/ -v
```
Expected: All backend tests pass

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "chore: final verification passes"
```
