from mt5.protocol import MT5Adapter


class AccountService:
    def __init__(self, adapter: MT5Adapter):
        self._adapter = adapter

    def get_account_info(self) -> dict:
        info = self._adapter.get_account_info()
        return {
            "balance": info.balance,
            "equity": info.equity,
            "margin": info.margin,
            "free_margin": info.free_margin,
            "margin_level": info.margin_level,
            "currency": info.currency,
            "name": info.name,
            "server": info.server,
            "leverage": info.leverage,
        }
