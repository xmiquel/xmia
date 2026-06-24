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
