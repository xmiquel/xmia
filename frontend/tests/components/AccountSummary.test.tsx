import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import AccountSummary from "../../src/components/AccountSummary";
import type { AccountInfo } from "../../src/types";

const mockAccount: AccountInfo = {
  balance: 10000,
  equity: 9500,
  margin: 500,
  free_margin: 9000,
  margin_level: 1900,
  currency: "USD",
  name: "Demo",
  server: "MetaQuotes-Demo",
  leverage: 100,
};

describe("AccountSummary", () => {
  it("shows loading state", () => {
    render(<AccountSummary account={null} loading={true} error={null} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(<AccountSummary account={null} loading={false} error="Connection failed" />);
    expect(screen.getByText(/Connection failed/i)).toBeInTheDocument();
  });

  it("renders account fields when data is provided", () => {
    render(<AccountSummary account={mockAccount} loading={false} error={null} />);
    expect(screen.getByText("$10,000.00")).toBeInTheDocument();
    expect(screen.getByText("$9,500.00")).toBeInTheDocument();
    expect(screen.getByText("$500.00")).toBeInTheDocument();
    expect(screen.getByText("$9,000.00")).toBeInTheDocument();
    expect(screen.getByText("1,900.00%")).toBeInTheDocument();
    expect(screen.getByText("USD")).toBeInTheDocument();
    expect(screen.getByText("100")).toBeInTheDocument();
  });
});
