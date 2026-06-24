import { fetchClient } from "./client";
import type { SymbolInfo } from "../types";

export function getSymbolInfo(symbol: string): Promise<SymbolInfo> {
  return fetchClient(`/api/v1/symbols/${encodeURIComponent(symbol)}`) as Promise<SymbolInfo>;
}
