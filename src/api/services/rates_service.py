import datetime

from mt5.protocol import MT5Adapter
from api.timeframes import parse_timeframe


class RatesService:
    def __init__(self, adapter: MT5Adapter):
        self._adapter = adapter

    def get_rates(self, symbol: str, timeframe: str, count: int) -> list[dict]:
        tf = parse_timeframe(timeframe)
        rates = self._adapter.get_rates(symbol, tf, count)
        return [
            {
                "time": r["time"].isoformat() if isinstance(r["time"], datetime.datetime) else r["time"],
                "open": r["open"],
                "high": r["high"],
                "low": r["low"],
                "close": r["close"],
                "volume": r["volume"],
            }
            for r in rates
        ]
