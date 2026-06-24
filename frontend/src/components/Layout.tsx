import { useState, useEffect, useCallback } from "react";
import Watchlist from "./Watchlist";
import PriceChart from "./PriceChart";
import AccountSummary from "./AccountSummary";
import TimeframeSelector from "./TimeframeSelector";
import { getAccountInfo } from "../api/account";
import { getRates } from "../api/rates";
import type { AccountInfo, Candle } from "../types";
import "./Layout.css";

const DEFAULT_SYMBOLS = ["EURUSD", "GBPUSD", "BTCUSD"];
const POLL_INTERVAL = 10_000;

export default function Layout() {
  const [selectedSymbol, setSelectedSymbol] = useState("EURUSD");
  const [timeframe, setTimeframe] = useState("PERIOD_H1");

  const [account, setAccount] = useState<AccountInfo | null>(null);
  const [accountLoading, setAccountLoading] = useState(true);
  const [accountError, setAccountError] = useState<string | null>(null);

  const [candles, setCandles] = useState<Candle[]>([]);
  const [candlesLoading, setCandlesLoading] = useState(true);
  const [candlesError, setCandlesError] = useState<string | null>(null);

  const fetchAccount = useCallback(async () => {
    try {
      setAccountLoading(true);
      setAccountError(null);
      const data = await getAccountInfo();
      setAccount(data);
    } catch (err) {
      setAccountError(err instanceof Error ? err.message : "Failed to load account");
    } finally {
      setAccountLoading(false);
    }
  }, []);

  const fetchRates = useCallback(async () => {
    try {
      setCandlesLoading(true);
      setCandlesError(null);
      const data = await getRates(selectedSymbol, timeframe, 100);
      setCandles(data);
    } catch (err) {
      setCandlesError(err instanceof Error ? err.message : "Failed to load rates");
    } finally {
      setCandlesLoading(false);
    }
  }, [selectedSymbol, timeframe]);

  useEffect(() => {
    fetchAccount();
    const interval = setInterval(fetchAccount, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchAccount]);

  useEffect(() => {
    fetchRates();
    const interval = setInterval(fetchRates, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchRates]);

  return (
    <div className="dashboard-layout">
      <Watchlist
        symbols={DEFAULT_SYMBOLS}
        selected={selectedSymbol}
        onSelect={setSelectedSymbol}
      />
      <div>
        <PriceChart
          data={candles}
          symbol={selectedSymbol}
          loading={candlesLoading}
          error={candlesError}
        />
        <TimeframeSelector value={timeframe} onChange={setTimeframe} />
      </div>
      <AccountSummary
        account={account}
        loading={accountLoading}
        error={accountError}
      />
    </div>
  );
}
