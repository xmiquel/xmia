from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass
class AccountInfo:
    balance: float
    equity: float
    margin: float
    free_margin: float
    margin_level: float
    currency: str
    name: str
    server: str
    leverage: int


@dataclass
class OrderResult:
    ticket: int
    filled_volume: float
    price: float
    comment: str


@dataclass
class PositionInfo:
    ticket: int
    symbol: str
    volume: float
    type_: int
    price_open: float
    sl: float
    tp: float
    profit: float
    swap: float
    comment: str


@dataclass
class DealInfo:
    ticket: int
    symbol: str
    volume: float
    type_: int
    price: float
    profit: float
    commission: float
    swap: float
    open_time: datetime
    close_time: datetime
    comment: str


@runtime_checkable
class MT5Adapter(Protocol):
    @property
    def is_connected(self) -> bool:
        ...

    @property
    def is_authenticated(self) -> bool:
        ...

    def initialize(
        self, path: str | None = None, login: int | None = None,
        password: str | None = None, server: str | None = None,
        portable: bool = False,
    ) -> None:
        ...

    def login(self, login: int, password: str, server: str) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def get_account_info(self) -> AccountInfo:
        ...

    def get_symbols(self) -> list[str]:
        ...

    def get_symbol_info(self, symbol: str) -> dict[str, object] | None:
        ...

    def get_rates(self, symbol: str, timeframe: int, count: int) -> list[dict[str, object]]:
        ...

    def get_rates_before(
        self, symbol: str, timeframe: int, count: int, before: int
    ) -> list[dict[str, object]]:
        ...

    def get_positions(self) -> list[PositionInfo]:
        ...

    def get_orders(self) -> list[dict[str, object]]:
        ...

    def send_order(
        self, symbol: str, volume: float, type_: int,
        price: float, sl: float = 0, tp: float = 0,
    ) -> OrderResult:
        ...

    def modify_order(self, ticket: int, price: float, sl: float, tp: float) -> None:
        ...

    def modify_position(self, ticket: int, sl: float, tp: float) -> None:
        ...

    def cancel_order(self, ticket: int) -> None:
        ...

    def get_history_deals(self, from_date: datetime, to_date: datetime) -> list[DealInfo]:
        ...
