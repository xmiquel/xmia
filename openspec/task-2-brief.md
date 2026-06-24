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
