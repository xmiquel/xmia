import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import DataWindow from "../../src/components/DataWindow";

const mockCandle = {
  time: 1780272000,
  open: 1.10000,
  high: 1.10500,
  low: 1.09500,
  close: 1.10200,
  tick_volume: 150,
  spread: 8,
  real_volume: 150000,
};

describe("DataWindow", () => {
  it("renders nothing when candle is null", () => {
    const { container } = render(
      <DataWindow candle={null} digits={5} position={{ x: 100, y: 200 }} />,
    );
    expect(container.innerHTML).toBe("");
  });

  it("renders nothing when position is null", () => {
    const { container } = render(
      <DataWindow candle={mockCandle} digits={5} position={null} />,
    );
    expect(container.innerHTML).toBe("");
  });

  it("displays Date, Time, OHLCV, Spread labels", () => {
    render(<DataWindow candle={mockCandle} digits={5} position={{ x: 100, y: 200 }} />);
    expect(screen.getByText("Date")).toBeInTheDocument();
    expect(screen.getByText("Time")).toBeInTheDocument();
    expect(screen.getByText("Open")).toBeInTheDocument();
    expect(screen.getByText("High")).toBeInTheDocument();
    expect(screen.getByText("Low")).toBeInTheDocument();
    expect(screen.getByText("Close")).toBeInTheDocument();
    expect(screen.getByText("Volume")).toBeInTheDocument();
    expect(screen.getByText("Tick Vol")).toBeInTheDocument();
    expect(screen.getByText("Spread")).toBeInTheDocument();
  });

  it("formats prices with correct precision", () => {
    render(<DataWindow candle={mockCandle} digits={5} position={{ x: 100, y: 200 }} />);
    expect(screen.getByText("1.10000")).toBeInTheDocument();
    expect(screen.getByText("1.10500")).toBeInTheDocument();
  });

  it("shows tick volume and spread values", () => {
    render(<DataWindow candle={mockCandle} digits={5} position={{ x: 100, y: 200 }} />);
    expect(screen.getAllByText("150")).toHaveLength(2);
    expect(screen.getByText("8")).toBeInTheDocument();
  });
});
