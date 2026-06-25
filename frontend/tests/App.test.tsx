import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../src/App";

vi.mock("../src/api/account", () => ({
  getAccountInfo: vi.fn().mockResolvedValue({
    balance: 10000,
    equity: 9500,
    margin: 500,
    free_margin: 9000,
    margin_level: 1900,
    currency: "USD",
    name: "Demo",
    server: "MetaQuotes-Demo",
    leverage: 100,
  }),
}));

vi.mock("../src/api/symbols", () => ({
  getSymbols: vi.fn().mockResolvedValue(["EURUSD", "GBPUSD", "BTCUSD"]),
  getSymbolInfo: vi.fn().mockResolvedValue({
    symbol: "EURUSD",
    digits: 5,
    spread: 10,
    margin_currency: "EUR",
    contract_size: 100000,
  }),
}));

vi.mock("../src/api/rates", () => ({
  getRates: vi.fn().mockResolvedValue([
    { time: 1780272000, open: 1.1, high: 1.11, low: 1.09, close: 1.105, tick_volume: 100, spread: 10, real_volume: 100000 },
  ]),
}));

describe("App", () => {
  it("renders the dashboard layout", async () => {
    render(<App />);
    expect(await screen.findByText("EURUSD")).toBeInTheDocument();
    expect(await screen.findByText("Account")).toBeInTheDocument();
  });
});
