from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto

from mt5.errors import AdapterNotConnectedError, AuthenticationError, TerminalNotAvailableError
from mt5.protocol import AccountInfo, DealInfo, OrderResult, PositionInfo


class AdapterState(Enum):
    DISCONNECTED = auto()
    INITIALIZED = auto()
    AUTHENTICATED = auto()


@dataclass
class FakeOrder:
    ticket: int
    symbol: str
    volume: float
    type_: int
    price: float
    sl: float
    tp: float
    comment: str = ""


@dataclass
class FakePosition:
    ticket: int
    symbol: str
    volume: float
    type_: int
    price_open: float
    sl: float
    tp: float
    profit: float = 0.0
    swap: float = 0.0
    comment: str = ""


@dataclass
class FakeDeal:
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
    comment: str = ""


class FakeMT5Adapter:
    def __init__(self, simulate_terminal_available: bool = True):
        self._state = AdapterState.DISCONNECTED
        self._ticket_counter: int = 1000
        self._orders: dict[int, FakeOrder] = {}
        self._positions: dict[int, FakePosition] = {}
        self._deals: list[FakeDeal] = []
        self._simulate_terminal_available = simulate_terminal_available
        self._error_modes: dict[str, type[Exception] | None] = {}
        self._terminal_path: str | None = None

    def set_error_mode(self, method: str, error: type[Exception] | None) -> None:
        self._error_modes[method] = error

    def _check_error(self, method: str) -> None:
        err = self._error_modes.get(method)
        if err is not None:
            raise err(f"Simulated error for {method}")

    def _require_state(self, *states: AdapterState) -> None:
        if self._state not in states:
            raise AdapterNotConnectedError(
                f"Adapter is {self._state.name}, expected {' or '.join(s.name for s in states)}"
            )

    @property
    def is_connected(self) -> bool:
        return self._state in (AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

    @property
    def is_authenticated(self) -> bool:
        return self._state == AdapterState.AUTHENTICATED

    def initialize(
        self, path: str | None = None, login: int | None = None,
        password: str | None = None, server: str | None = None,
        portable: bool = False,
    ) -> None:
        self._check_error("initialize")
        if not self._simulate_terminal_available:
            raise TerminalNotAvailableError("MT5 terminal is not available")

        self._state = AdapterState.INITIALIZED
        self._terminal_path = path

        if login is not None and password is not None and server is not None:
            self._state = AdapterState.AUTHENTICATED

    def login(self, login: int, password: str, server: str) -> None:
        self._check_error("login")
        self._require_state(AdapterState.INITIALIZED)

        if password == "wrong":  # noqa: S105  # nosec
            raise AuthenticationError("Invalid account number or password")

        self._state = AdapterState.AUTHENTICATED

    def shutdown(self) -> None:
        self._state = AdapterState.DISCONNECTED
        self._terminal_path = None

    def get_account_info(self) -> AccountInfo:
        self._check_error("get_account_info")
        self._require_state(AdapterState.AUTHENTICATED)

        return AccountInfo(
            balance=10000.0,
            equity=9500.0,
            margin=500.0,
            free_margin=9000.0,
            margin_level=1900.0,
            currency="USD",
            name="Fake Account",
            server="FakeServer-Demo",
            leverage=100,
        )

    def get_symbol_info(self, symbol: str) -> dict[str, object] | None:
        self._check_error("get_symbol_info")
        self._require_state(AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

        known_symbols = {
            "EURUSD": {"digits": 5, "spread": 10,
            "margin_currency": "EUR", "contract_size": 100000},
            "GBPUSD": {"digits": 5, "spread": 12,
            "margin_currency": "GBP", "contract_size": 100000},
        }
        return known_symbols.get(symbol.upper())

    def get_rates(self, symbol: str, timeframe: int, count: int) -> list[dict[str, object]]:
        self._check_error("get_rates")
        self._require_state(AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

        now = datetime.now()
        rates = []
        for i in range(count):
            t = now - timedelta(hours=timeframe * i)
            base = 1.1000 + i * 0.0001
            rates.append({
                "time": int(t.timestamp()),
                "open": base,
                "high": base + 0.0005,
                "low": base - 0.0005,
                "close": base + 0.0002,
                "tick_volume": 100 + i * 10,
                "spread": 5 + (i % 15),
                "real_volume": (100 + i * 10) * 1000,
            })
        return rates

    def get_rates_before(
        self, symbol: str, timeframe: int, count: int, before: int
    ) -> list[dict[str, object]]:
        self._check_error("get_rates_before")
        self._require_state(AdapterState.INITIALIZED, AdapterState.AUTHENTICATED)

        rates = []
        current_time = before - 1
        for i in range(count):
            t = datetime.fromtimestamp(current_time) - timedelta(hours=timeframe * i)
            base = 1.1000 - (i * 0.0001)
            rates.append({
                "time": int(t.timestamp()),
                "open": base,
                "high": base + 0.0005,
                "low": base - 0.0005,
                "close": base + 0.0002,
                "tick_volume": 100 + i * 10,
                "spread": 5 + (i % 15),
                "real_volume": (100 + i * 10) * 1000,
            })
        return [r for r in rates if r["time"] < before]

    def get_positions(self) -> list[PositionInfo]:
        self._check_error("get_positions")
        self._require_state(AdapterState.AUTHENTICATED)

        return [
            PositionInfo(
                ticket=pos.ticket,
                symbol=pos.symbol,
                volume=pos.volume,
                type_=pos.type_,
                price_open=pos.price_open,
                sl=pos.sl,
                tp=pos.tp,
                profit=pos.profit,
                swap=pos.swap,
                comment=pos.comment,
            )
            for pos in self._positions.values()
        ]

    def get_orders(self) -> list[dict[str, object]]:
        self._check_error("get_orders")
        self._require_state(AdapterState.AUTHENTICATED)

        return [
            {
                "ticket": order.ticket,
                "symbol": order.symbol,
                "volume": order.volume,
                "type_": order.type_,
                "price": order.price,
                "sl": order.sl,
                "tp": order.tp,
            }
            for order in self._orders.values()
        ]

    def send_order(
        self, symbol: str, volume: float, type_: int,
        price: float, sl: float = 0, tp: float = 0,
    ) -> OrderResult:
        self._check_error("send_order")
        self._require_state(AdapterState.AUTHENTICATED)

        self._ticket_counter += 1
        ticket = self._ticket_counter

        order = FakeOrder(
            ticket=ticket,
            symbol=symbol,
            volume=volume,
            type_=type_,
            price=price,
            sl=sl,
            tp=tp,
        )

        if type_ == 0:
            position = FakePosition(
                ticket=ticket,
                symbol=symbol,
                volume=volume,
                type_=type_,
                price_open=price,
                sl=sl,
                tp=tp,
            )
            self._positions[ticket] = position
        else:
            self._orders[ticket] = order

        return OrderResult(ticket=ticket, filled_volume=volume, price=price, comment="done")

    def modify_order(self, ticket: int, price: float, sl: float, tp: float) -> None:
        self._check_error("modify_order")
        self._require_state(AdapterState.AUTHENTICATED)

        if ticket not in self._orders:
            raise ValueError(f"Order {ticket} not found")

        order = self._orders[ticket]
        order.price = price
        order.sl = sl
        order.tp = tp

    def modify_position(self, ticket: int, sl: float, tp: float) -> None:
        self._check_error("modify_position")
        self._require_state(AdapterState.AUTHENTICATED)

        if ticket not in self._positions:
            raise ValueError(f"Position {ticket} not found")

        pos = self._positions[ticket]
        pos.sl = sl
        pos.tp = tp

    def cancel_order(self, ticket: int) -> None:
        self._check_error("cancel_order")
        self._require_state(AdapterState.AUTHENTICATED)

        if ticket not in self._orders:
            raise ValueError(f"Order {ticket} not found")

        del self._orders[ticket]

    def get_history_deals(self, from_date: datetime, to_date: datetime) -> list[DealInfo]:
        self._check_error("get_history_deals")
        self._require_state(AdapterState.AUTHENTICATED)

        if from_date > to_date:
            raise ValueError("from_date must be before to_date")

        return [
            DealInfo(
                ticket=d.ticket,
                symbol=d.symbol,
                volume=d.volume,
                type_=d.type_,
                price=d.price,
                profit=d.profit,
                commission=d.commission,
                swap=d.swap,
                open_time=d.open_time,
                close_time=d.close_time,
                comment=d.comment,
            )
            for d in self._deals
            if from_date <= d.close_time <= to_date
        ]
