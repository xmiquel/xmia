from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from api.dependencies import get_adapter
from api.services.rates_service import RatesService
from api.timeframes import VALID_TIMEFRAMES
from mt5.protocol import MT5Adapter

router = APIRouter(tags=["Rates"])


def _validate_timeframe(
    timeframe: str = Query("PERIOD_H1", description="MT5 timeframe constant"),
) -> str:
    if timeframe.upper() not in VALID_TIMEFRAMES:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid timeframe '{timeframe}'. Valid options: {', '.join(VALID_TIMEFRAMES)}",
        )
    return timeframe


@router.get("/api/v1/rates/{symbol}")
async def get_rates(
    symbol: str = Path(..., min_length=1, max_length=20),
    timeframe: str = Depends(_validate_timeframe),
    count: int = Query(10, ge=1, le=1000, description="Number of candles (max 1000)"),
    adapter: MT5Adapter = Depends(get_adapter),
):
    service = RatesService(adapter)
    return service.get_rates(symbol, timeframe, count)
