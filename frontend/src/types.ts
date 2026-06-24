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
