import type { AccountInfo } from "../types";
import "./AccountSummary.css";

interface Props {
  account: AccountInfo | null;
  loading: boolean;
  error: string | null;
}

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
  }).format(value);
}

function formatPercent(value: number): string {
  return `${value.toLocaleString("en-US", { minimumFractionDigits: 2 })}%`;
}

export default function AccountSummary({ account, loading, error }: Props) {
  if (loading) return <div className="account-summary"><div className="loading">Loading account...</div></div>;
  if (error) return <div className="account-summary"><div className="error">{error}</div></div>;
  if (!account) return <div className="account-summary"><div className="loading">No account data</div></div>;

  return (
    <div className="account-summary">
      <h2>Account</h2>
      <div className="field">
        <span className="field-label">Balance</span>
        <span className="field-value">{formatCurrency(account.balance, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Equity</span>
        <span className="field-value">{formatCurrency(account.equity, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Margin</span>
        <span className="field-value">{formatCurrency(account.margin, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Free Margin</span>
        <span className="field-value">{formatCurrency(account.free_margin, account.currency)}</span>
      </div>
      <div className="field">
        <span className="field-label">Margin Level</span>
        <span className="field-value">{formatPercent(account.margin_level)}</span>
      </div>
      <div className="field">
        <span className="field-label">Currency</span>
        <span className="field-value">{account.currency}</span>
      </div>
      <div className="field">
        <span className="field-label">Leverage</span>
        <span className="field-value">{account.leverage}</span>
      </div>
    </div>
  );
}
