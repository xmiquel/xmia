import type { Candle } from "../types";
import "./DataWindow.css";

interface Props {
  candle: Candle | null;
  digits: number;
  position: { x: number; y: number } | null;
}

export default function DataWindow({ candle, digits, position }: Props) {
  if (!candle || !position) return null;

  const fmt = (v: number) => v.toFixed(digits);
  const d = new Date(candle.time * 1000);
  const dateStr = d.toISOString().slice(0, 10);
  const timeStr = d.toTimeString().slice(0, 8);

  const style: React.CSSProperties = {
    position: "absolute",
    left: position.x + 15,
    top: position.y - 80,
    pointerEvents: "none",
    zIndex: 100,
    background: "rgba(0,0,0,0.85)",
    color: "#fff",
    fontFamily: "'Courier New', monospace",
    fontSize: "11px",
    padding: "6px 10px",
    borderRadius: "3px",
    lineHeight: 1.6,
    whiteSpace: "nowrap",
  };

  return (
    <div className="data-window" style={style}>
      <Row label="Date" value={dateStr} />
      <Row label="Time" value={timeStr} />
      <Divider />
      <Row label="Open" value={fmt(candle.open)} />
      <Row label="High" value={fmt(candle.high)} />
      <Row label="Low" value={fmt(candle.low)} />
      <Row label="Close" value={fmt(candle.close)} />
      <Divider />
      <Row label="Volume" value={String(candle.tick_volume)} />
      <Row label="Tick Vol" value={String(candle.tick_volume)} />
      <Row label="Spread" value={String(candle.spread)} />
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="dw-row">
      <span className="dw-label">{label}</span>
      <span className="dw-value">{value}</span>
    </div>
  );
}

function Divider() {
  return <div className="dw-divider" />;
}
