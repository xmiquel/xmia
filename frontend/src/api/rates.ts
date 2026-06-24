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
