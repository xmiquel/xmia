from api.timeframes import parse_timeframe
from mt5.protocol import MT5Adapter


class RatesService:
    def __init__(self, adapter: MT5Adapter):
        self._adapter = adapter

    def get_rates(self, symbol: str, timeframe: str, count: int) -> list[dict]:
        tf = parse_timeframe(timeframe)
        return self._adapter.get_rates(symbol, tf, count)
