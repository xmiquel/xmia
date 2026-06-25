import { useEffect, useRef, useState } from "react";
import { createChart, ColorType } from "lightweight-charts";
import type { IChartApi, ISeriesApi, UTCTimestamp } from "lightweight-charts";
import type { Candle } from "../types";
import DataWindow from "./DataWindow";
import "./PriceChart.css";

interface Props {
  data: Candle[];
  symbol: string;
  digits: number;
  loading: boolean;
  error: string | null;
  onVisibleRangeChange?: (from: number, to: number) => void;
}

export default function PriceChart({ data, symbol, digits, loading, error, onVisibleRangeChange }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const symbolRef = useRef(symbol);
  const dataMapRef = useRef<Map<number, Candle>>(new Map());
  const visibleRangeCbRef = useRef(onVisibleRangeChange);
  const [hoveredCandle, setHoveredCandle] = useState<Candle | null>(null);
  const [tooltipPos, setTooltipPos] = useState<{ x: number; y: number } | null>(null);

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

    chart.subscribeCrosshairMove((param) => {
      if (!param.time || !param.point) {
        setHoveredCandle(null);
        setTooltipPos(null);
        return;
      }
      const candle = dataMapRef.current.get(param.time as number);
      if (candle) {
        setTooltipPos({ x: param.point.x, y: param.point.y });
        setHoveredCandle(candle);
      }
    });

    chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
      if (range && visibleRangeCbRef.current) {
        visibleRangeCbRef.current(range.from, range.to);
      }
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
    visibleRangeCbRef.current = onVisibleRangeChange;
  }, [onVisibleRangeChange]);

  useEffect(() => {
    const series = seriesRef.current;
    if (!series || data.length === 0) return;

    const map = new Map<number, Candle>();
    data.forEach((c) => map.set(c.time, c));
    dataMapRef.current = map;

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
      setHoveredCandle(null);
      setTooltipPos(null);
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
    <div className="price-chart" style={{ position: "relative" }}>
      <h2>{symbol}</h2>
      <div className="chart-container" ref={chartContainerRef}>
        <DataWindow candle={hoveredCandle} digits={digits} position={tooltipPos} />
      </div>
      {loading && <div className="loading">Loading chart...</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}
