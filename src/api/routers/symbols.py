from fastapi import APIRouter, Depends, Path

from api.dependencies import get_adapter
from api.services.symbols_service import SymbolsService
from mt5.protocol import MT5Adapter

router = APIRouter(tags=["Symbols"])


@router.get("/api/v1/symbols/{symbol}")
async def get_symbol(
    symbol: str = Path(..., min_length=1, max_length=20),
    adapter: MT5Adapter = Depends(get_adapter),
):
    service = SymbolsService(adapter)
    return service.get_symbol_info(symbol)
