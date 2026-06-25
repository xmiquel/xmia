import { fetchClient } from "./client";
import type { SymbolInfo } from "../types";

export function getSymbols(): Promise<string[]> {
  return fetchClient("/api/v1/symbols") as Promise<string[]>;
}

export function getSymbolInfo(symbol: string): Promise<SymbolInfo> {
  return fetchClient(`/api/v1/symbols/${encodeURIComponent(symbol)}`) as Promise<SymbolInfo>;
}
