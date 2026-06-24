import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TimeframeSelector from "../../src/components/TimeframeSelector";

describe("TimeframeSelector", () => {
  it("renders all timeframe buttons", () => {
    render(<TimeframeSelector value="PERIOD_H1" onChange={() => {}} />);
    expect(screen.getByText("M1")).toBeInTheDocument();
    expect(screen.getByText("M5")).toBeInTheDocument();
    expect(screen.getByText("H1")).toBeInTheDocument();
    expect(screen.getByText("H4")).toBeInTheDocument();
    expect(screen.getByText("D1")).toBeInTheDocument();
  });

  it("highlights the active timeframe", () => {
    render(<TimeframeSelector value="PERIOD_H1" onChange={() => {}} />);
    expect(screen.getByText("H1")).toHaveClass("active");
  });

  it("calls onChange with the timeframe constant when clicked", () => {
    const onChange = vi.fn();
    render(<TimeframeSelector value="PERIOD_H1" onChange={onChange} />);
    fireEvent.click(screen.getByText("M5"));
    expect(onChange).toHaveBeenCalledWith("PERIOD_M5");
  });
});
