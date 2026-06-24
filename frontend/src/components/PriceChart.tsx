import { useEffect, useRef } from "react";
import { createChart, ColorType } from "lightweight-charts";
import type { IChartApi, ISeriesApi, UTCTimestamp } from "lightweight-charts";
import type { Candle } from "../types";
import "./PriceChart.css";

interface Props {
  data: Candle[];
  symbol: string;
  digits: number;
  loading: boolean;
  error: string | null;
}

export default function PriceChart({ data, symbol, digits, loading, error }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const symbolRef = useRef(symbol);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { type: ColorType.Solid, color: "#ffffff" },
        textColor: "#333",
      },
      grid: {
        vertLines: { color: "#f0f0f0" },
        horzLines: { color: "#f0f0f0" },
      },
      crosshair: {
        mode: 0,
      },
      timeScale: {
        borderColor: "#e0e0e0",
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const series = chart.addCandlestickSeries({
      upColor: "transparent",
      downColor: "#000000",
      borderDownColor: "#000000",
      borderUpColor: "#000000",
      wickDownColor: "#000000",
      wickUpColor: "#000000",
    });

    chartRef.current = chart;
    seriesRef.current = series;

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    const series = seriesRef.current;
    if (!series || data.length === 0) return;

    series.setData(
      data.map((c) => ({
        time: c.time as UTCTimestamp,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      })),
    );

    const isNewSymbol = symbol !== symbolRef.current;
    symbolRef.current = symbol;

    if (isNewSymbol) {
      chartRef.current?.timeScale().fitContent();
    }
  }, [data, symbol]);

  useEffect(() => {
    seriesRef.current?.applyOptions({
      priceFormat: {
        type: "price" as const,
        precision: digits,
        minMove: 1 / Math.pow(10, digits),
      },
    });
  }, [digits]);

  return (
    <div className="price-chart">
      <h2>{symbol}</h2>
      <div className="chart-container" ref={chartContainerRef} />
      {loading && <div className="loading">Loading chart...</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}
