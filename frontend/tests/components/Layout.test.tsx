import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Layout from "../../src/components/Layout";

vi.mock("../../src/api/account", () => ({
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

vi.mock("../../src/api/rates", () => ({
  getRates: vi.fn().mockResolvedValue([
    { time: "2026-06-18", open: 1.1, high: 1.11, low: 1.09, close: 1.105, volume: 100 },
  ]),
}));

describe("Layout", () => {
  it("renders all three panels", () => {
    render(<Layout />);
    expect(screen.getByText("EURUSD")).toBeInTheDocument();
    expect(screen.getByText("GBPUSD")).toBeInTheDocument();
    expect(screen.getByText("BTCUSD")).toBeInTheDocument();
  });
});
