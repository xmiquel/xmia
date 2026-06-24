import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import PriceChart from "../../src/components/PriceChart";
import type { Candle } from "../../src/types";

const mockCandles: Candle[] = [
  { time: 1780272000, open: 1.1, high: 1.11, low: 1.09, close: 1.105, volume: 100 },
];

describe("PriceChart", () => {
  it("shows loading state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" digits={5} loading={true} error={null} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(<PriceChart data={[]} symbol="EURUSD" digits={5} loading={false} error="Rates unavailable" />);
    expect(screen.getByText(/Rates unavailable/i)).toBeInTheDocument();
  });

  it("renders chart container when data is provided", () => {
    const { container } = render(
      <PriceChart data={mockCandles} symbol="EURUSD" digits={5} loading={false} error={null} />,
    );
    expect(container.querySelector(".price-chart")).toBeInTheDocument();
  });
});
