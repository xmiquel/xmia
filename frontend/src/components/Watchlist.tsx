import "./Watchlist.css";

interface Props {
  symbols: string[];
  selected: string;
  onSelect: (symbol: string) => void;
}

export default function Watchlist({ symbols, selected, onSelect }: Props) {
  return (
    <div className="watchlist">
      <h2>Symbols</h2>
      <ul>
        {symbols.map((s) => (
          <li
            key={s}
            className={s === selected ? "selected" : ""}
            onClick={() => onSelect(s)}
          >
            {s}
          </li>
        ))}
      </ul>
    </div>
  );
}
