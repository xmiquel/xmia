import "./TimeframeSelector.css";

const TIMEFRAMES = [
  { label: "M1", value: "PERIOD_M1" },
  { label: "M5", value: "PERIOD_M5" },
  { label: "M15", value: "PERIOD_M15" },
  { label: "M30", value: "PERIOD_M30" },
  { label: "H1", value: "PERIOD_H1" },
  { label: "H4", value: "PERIOD_H4" },
  { label: "D1", value: "PERIOD_D1" },
  { label: "W1", value: "PERIOD_W1" },
  { label: "MN1", value: "PERIOD_MN1" },
];

interface Props {
  value: string;
  onChange: (timeframe: string) => void;
}

export default function TimeframeSelector({ value, onChange }: Props) {
  return (
    <div className="timeframe-selector">
      {TIMEFRAMES.map((tf) => (
        <button
          key={tf.value}
          className={value === tf.value ? "active" : ""}
          onClick={() => onChange(tf.value)}
        >
          {tf.label}
        </button>
      ))}
    </div>
  );
}
