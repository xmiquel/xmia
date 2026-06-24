from fastapi import APIRouter, Depends

from api.dependencies import get_adapter
from api.services.account_service import AccountService
from mt5.protocol import MT5Adapter

router = APIRouter(tags=["Account"])


@router.get("/api/v1/account")
async def get_account(adapter: MT5Adapter = Depends(get_adapter)):
    service = AccountService(adapter)
    return service.get_account_info()
