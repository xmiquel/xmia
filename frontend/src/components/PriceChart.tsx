import { useEffect, useRef } from "react";
import { createChart, ColorType } from "lightweight-charts";
import type { Candle } from "../types";
import "./PriceChart.css";

interface Props {
  data: Candle[];
  symbol: string;
  loading: boolean;
  error: string | null;
}

export default function PriceChart({ data, symbol, loading, error }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

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
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderDownColor: "#ef5350",
      borderUpColor: "#26a69a",
      wickDownColor: "#ef5350",
      wickUpColor: "#26a69a",
    });

    candleSeries.setData(
      data.map((c) => ({
        time: c.time,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      })),
    );

    chart.timeScale().fitContent();

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [data]);

  if (loading) return <div className="price-chart"><div className="loading">Loading chart...</div></div>;
  if (error) return <div className="price-chart"><div className="error">{error}</div></div>;

  return (
    <div className="price-chart">
      <h2>{symbol}</h2>
      <div className="chart-container" ref={chartContainerRef} />
    </div>
  );
}
