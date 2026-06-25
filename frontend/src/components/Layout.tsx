import { useState, useEffect, useCallback, useRef } from "react";
import Watchlist from "./Watchlist";
import PriceChart from "./PriceChart";
import AccountSummary from "./AccountSummary";
import TimeframeSelector from "./TimeframeSelector";
import { getAccountInfo } from "../api/account";
import { getSymbolInfo } from "../api/symbols";
import { getRates, getRatesBeforeSymbol } from "../api/rates";
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

  const [allCandles, setAllCandles] = useState<Candle[]>([]);
  const [candlesLoading, setCandlesLoading] = useState(true);
  const [candlesError, setCandlesError] = useState<string | null>(null);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const isLoadingMoreRef = useRef(false);
  const hasMoreRef = useRef(true);
  const allCandlesRef = useRef<Candle[]>([]);
  const symbolRef = useRef(selectedSymbol);
  const timeframeRef = useRef(timeframe);
  const pendingBeforeRef = useRef<number | null>(null);

  isLoadingMoreRef.current = isLoadingMore;
  hasMoreRef.current = hasMore;
  allCandlesRef.current = allCandles;
  symbolRef.current = selectedSymbol;
  timeframeRef.current = timeframe;

  const [digits, setDigits] = useState(5);

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

  const fetchSymbolInfo = useCallback(async () => {
    try {
      const info = await getSymbolInfo(selectedSymbol);
      if (info?.digits) {
        setDigits(info.digits);
      }
    } catch {
      setDigits(5);
    }
  }, [selectedSymbol]);

  const fetchRates = useCallback(async () => {
    try {
      setCandlesLoading(true);
      setCandlesError(null);
      const data = await getRates(selectedSymbol, timeframe, 100);
      setAllCandles((prev) => {
        const map = new Map(prev.map((c) => [c.time, c]));
        for (const candle of data) {
          map.set(candle.time, candle);
        }
        return Array.from(map.values()).sort((a, b) => a.time - b.time);
      });
    } catch (err) {
      setCandlesError(err instanceof Error ? err.message : "Failed to load rates");
    } finally {
      setCandlesLoading(false);
    }
  }, [selectedSymbol, timeframe]);

  useEffect(() => {
    setAllCandles([]);
    setHasMore(true);
    setIsLoadingMore(false);
    setCandlesError(null);
    pendingBeforeRef.current = null;
  }, [selectedSymbol, timeframe]);

  const handleVisibleRangeChange = useCallback(
    async (from: number) => {
      if (isLoadingMoreRef.current || !hasMoreRef.current || allCandlesRef.current.length === 0) return;
      const totalBars = allCandlesRef.current.length;
      const threshold = totalBars * 0.15;
      if (from > threshold) return;

      const earliest = allCandlesRef.current[0].time;
      if (earliest === pendingBeforeRef.current) return;

      pendingBeforeRef.current = earliest;
      isLoadingMoreRef.current = true;
      setIsLoadingMore(true);
      try {
        const olderCandles = await getRatesBeforeSymbol(
          symbolRef.current,
          timeframeRef.current,
          500,
          earliest,
        );
        if (olderCandles.length === 0) {
          setHasMore(false);
          hasMoreRef.current = false;
        } else {
          const existingTimes = new Set(allCandlesRef.current.map((c) => c.time));
          const uniqueOlder = olderCandles.filter((c) => !existingTimes.has(c.time));
          if (uniqueOlder.length > 0) {
            setAllCandles((prev) => [...uniqueOlder, ...prev].sort((a, b) => a.time - b.time));
          }
        }
      } catch {
        // silent — TradingView-style
      } finally {
        isLoadingMoreRef.current = false;
        setIsLoadingMore(false);
      }
    },
    [],
  );

  useEffect(() => {
    fetchAccount();
    const interval = setInterval(fetchAccount, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchAccount]);

  useEffect(() => {
    fetchRates();
    fetchSymbolInfo();
    const interval = setInterval(fetchRates, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchRates, fetchSymbolInfo]);

  return (
    <div className="dashboard-layout">
      <Watchlist
        symbols={DEFAULT_SYMBOLS}
        selected={selectedSymbol}
        onSelect={setSelectedSymbol}
      />
      <div>
        <PriceChart
          data={allCandles}
          symbol={selectedSymbol}
          digits={digits}
          loading={candlesLoading}
          error={candlesError}
          onVisibleRangeChange={handleVisibleRangeChange}
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
