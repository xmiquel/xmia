from datetime import datetime
from typing import TYPE_CHECKING, Any

from mt5.errors import (
    AdapterNotConnectedError,
    AuthenticationError,
    ConnectionError,
    TerminalNotAvailableError,
)
from mt5.protocol import AccountInfo, DealInfo, OrderResult, PositionInfo

if TYPE_CHECKING:
    pass


class LiveMT5Adapter:
    def __init__(self) -> None:
        self._mt5 = None
        self._connected = False
        self._authenticated = False

    def _import_mt5(self) -> Any:
        if self._mt5 is not None:
            return self._mt5
        try:
            import MetaTrader5 as mt5  # noqa: N813
            self._mt5 = mt5
        except ImportError:
            raise TerminalNotAvailableError("MetaTrader5 module is not available on this platform")
        return self._mt5

    def _translate_retcode(self, result: object, success_code: int = 1) -> None:
        mt5 = self._import_mt5()
        if isinstance(result, (int, bool)) and result == success_code:
            return
        if isinstance(result, (int, bool)):
            error = mt5.last_error() if hasattr(mt5, "last_error") else (0, "unknown")
            if error[1] and "auth" in str(error[1]).lower():
                raise AuthenticationError(f"Authentication failed: {error[1]}")
            raise ConnectionError(f"MT5 operation failed: {error[1]}")
        if result is None:
            error = mt5.last_error() if hasattr(mt5, "last_error") else (0, "unknown")
            raise ConnectionError(f"MT5 operation returned None: {error[1]}")

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_authenticated(self) -> bool:
        return self._authenticated

    def initialize(
        self, path: str | None = None, login: int | None = None,
        password: str | None = None, server: str | None = None,
        portable: bool = False,
    ) -> None:
        mt5 = self._import_mt5()
        kwargs: dict[str, Any] = {}
        if path is not None:
            kwargs["path"] = path
        if login is not None:
            kwargs["login"] = login
        if password is not None:
            kwargs["password"] = password
        if server is not None:
            kwargs["server"] = server
        if portable:
            kwargs["portable"] = True
        try:
            result = mt5.initialize(**kwargs)
        except Exception as e:
            raise TerminalNotAvailableError(f"Failed to initialize MT5 terminal: {e}")

        if not result:
            error = mt5.last_error() if hasattr(mt5, "last_error") else (0, "unknown")
            raise TerminalNotAvailableError(f"Failed to initialize MT5 terminal: {error}")

        self._connected = True

        if login is not None and password is not None and server is not None:
            self._authenticated = True

    def login(self, login: int, password: str, server: str) -> None:
        mt5 = self._import_mt5()
        if not self._connected:
            raise AdapterNotConnectedError("MT5 terminal is not initialized")

        result = mt5.login(login=login, password=password, server=server)
        if not result:
            error = mt5.last_error() if hasattr(mt5, "last_error") else (0, "unknown")
            raise AuthenticationError(f"Login failed: {error}")

        self._authenticated = True

    def shutdown(self) -> None:
        if not self._connected:
            return
        try:
            mt5 = self._import_mt5()
            mt5.shutdown()
        except Exception:
            self._logger.exception("Error during MT5 shutdown")
        finally:
            self._connected = False
            self._authenticated = False

    def get_account_info(self) -> AccountInfo:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        info = mt5.account_info()
        if info is None:
            raise ConnectionError("Failed to get account info")

        return AccountInfo(
            balance=info.balance,
            equity=info.equity,
            margin=info.margin,
            free_margin=info.margin_free,
            margin_level=info.margin_level,
            currency=info.currency,
            name=info.name,
            server=info.server,
            leverage=info.leverage,
        )

    def get_symbol_info(self, symbol: str) -> dict[str, object] | None:
        mt5 = self._import_mt5()
        if not self._connected:
            raise AdapterNotConnectedError("Not connected")

        info = mt5.symbol_info(symbol)
        if info is None:
            return None

        return {
            "digits": info.digits,
            "spread": info.spread,
            "margin_currency": info.currency_margin,
            "contract_size": info.trade_contract_size,
        }

    def get_rates(self, symbol: str, timeframe: int, count: int) -> list[dict[str, object]]:
        mt5 = self._import_mt5()
        if not self._connected:
            raise AdapterNotConnectedError("Not connected")

        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            return []

        return [
            {
                "time": int(r[0]),
                "open": float(r[1]),
                "high": float(r[2]),
                "low": float(r[3]),
                "close": float(r[4]),
                "tick_volume": int(r[5]),
                "spread": int(r[6]),
                "real_volume": int(r[7]),
            }
            for r in rates
        ]

    def get_rates_before(
        self, symbol: str, timeframe: int, count: int, before: int
    ) -> list[dict[str, object]]:
        mt5 = self._import_mt5()
        if not self._connected:
            raise AdapterNotConnectedError("Not connected")

        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_from(symbol, timeframe, before, count)
        if rates is None:
            return []

        return [
            {
                "time": int(r[0]),
                "open": float(r[1]),
                "high": float(r[2]),
                "low": float(r[3]),
                "close": float(r[4]),
                "tick_volume": int(r[5]),
                "spread": int(r[6]),
                "real_volume": int(r[7]),
            }
            for r in rates
            if int(r[0]) < before
        ]

    def get_positions(self) -> list[PositionInfo]:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        positions = mt5.positions_get()
        if positions is None:
            return []

        return [
            PositionInfo(
                ticket=p.ticket,
                symbol=p.symbol,
                volume=p.volume,
                type_=p.type,
                price_open=p.price_open,
                sl=p.sl,
                tp=p.tp,
                profit=p.profit,
                swap=p.swap,
                comment=p.comment,
            )
            for p in positions
        ]

    def get_orders(self) -> list[dict[str, object]]:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        orders = mt5.orders_get()
        if orders is None:
            return []

        return [
            {
                "ticket": o.ticket,
                "symbol": o.symbol,
                "volume": o.volume_initial,
                "type_": o.type,
                "price": o.price_open,
                "sl": o.sl,
                "tp": o.tp,
            }
            for o in orders
        ]

    def send_order(
        self, symbol: str, volume: float, type_: int,
        price: float, sl: float = 0, tp: float = 0,
    ) -> OrderResult:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        request = {
            "action": mt5.TRADE_ACTION_DEAL if type_ == 0 else mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY if type_ == 0 else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            error_code = result.retcode if result else "unknown"
            raise ConnectionError(f"Order failed with code: {error_code}")

        return OrderResult(
            ticket=result.order,
            filled_volume=result.volume,
            price=result.price,
            comment=result.comment,
        )

    def modify_order(self, ticket: int, price: float, sl: float, tp: float) -> None:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "order": ticket,
            "price": price,
            "sl": sl,
            "tp": tp,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            error_code = result.retcode if result else "unknown"
            raise ConnectionError(f"Modify order failed with code: {error_code}")

    def modify_position(self, ticket: int, sl: float, tp: float) -> None:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        positions = mt5.positions_get(ticket=ticket)
        if positions is None or len(positions) == 0:
            raise ValueError(f"Position {ticket} not found")

        pos = positions[0]
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": sl,
            "tp": tp,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            error_code = result.retcode if result else "unknown"
            raise ConnectionError(f"Modify position failed with code: {error_code}")

    def cancel_order(self, ticket: int) -> None:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            error_code = result.retcode if result else "unknown"
            raise ConnectionError(f"Cancel order failed with code: {error_code}")

    def get_history_deals(self, from_date: datetime, to_date: datetime) -> list[DealInfo]:
        mt5 = self._import_mt5()
        if not self._authenticated:
            raise AdapterNotConnectedError("Not authenticated")

        if from_date > to_date:
            raise ValueError("from_date must be before to_date")

        deals = mt5.history_deals_get(from_date, to_date)
        if deals is None:
            return []

        return [
            DealInfo(
                ticket=d.ticket,
                symbol=d.symbol,
                volume=d.volume,
                type_=d.type,
                price=d.price,
                profit=d.profit,
                commission=d.commission,
                swap=d.swap,
                open_time=datetime.fromtimestamp(d.time),
                close_time=datetime.fromtimestamp(d.time_close),
                comment=d.comment,
            )
            for d in deals
        ]
