from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from mt5.protocol import MT5Adapter


class SymbolsService:
    def __init__(self, adapter: MT5Adapter):
        self._adapter = adapter

    def get_symbols(self) -> list[str]:
        return self._adapter.get_symbols()

    def get_symbol_info(self, symbol: str) -> dict:
        info = self._adapter.get_symbol_info(symbol)
        if info is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Symbol '{symbol}' not found",
            )
        return {
            "symbol": symbol.upper(),
            "digits": info["digits"],
            "spread": info["spread"],
            "margin_currency": info["margin_currency"],
            "contract_size": info["contract_size"],
        }
