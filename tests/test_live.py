from unittest.mock import MagicMock, patch

import pytest

from mt5.errors import (
    AdapterNotConnectedError,
    AuthenticationError,
    ConnectionError,
    TerminalNotAvailableError,
)


class TestLiveMT5AdapterLazyImport:
    def test_constructor_does_not_import_mt5(self):
        from mt5.live import LiveMT5Adapter
        adapter = LiveMT5Adapter()
        assert adapter._mt5 is None

    def test_initialize_imports_mt5(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize()
        assert adapter.is_connected

    def test_lazy_import_on_non_windows(self):
        import sys
        if "MetaTrader5" in sys.modules:
            del sys.modules["MetaTrader5"]
        from mt5.live import LiveMT5Adapter
        adapter = LiveMT5Adapter()
        assert not adapter.is_connected
        assert not adapter.is_authenticated


class TestLiveMT5AdapterInitialize:
    def test_initialize_success(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize()
        assert adapter.is_connected
        mt5_mock.initialize.assert_called_once()

    def test_initialize_failure_raises(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = False
        with pytest.raises(TerminalNotAvailableError):
            adapter.initialize()
        assert not adapter.is_connected

    def test_initialize_with_path(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize(path="C:/MT5")
        mt5_mock.initialize.assert_called_once_with(path="C:/MT5")

    def test_initialize_with_credentials(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize(login=12345, password="pass", server="srv")
        mt5_mock.initialize.assert_called_once_with(login=12345, password="pass", server="srv")
        assert adapter.is_authenticated

    def test_initialize_exception_raises(self, mt5_mock, adapter):
        mt5_mock.initialize.side_effect = Exception("timeout")
        with pytest.raises(TerminalNotAvailableError):
            adapter.initialize()


class TestLiveMT5AdapterLogin:
    def test_login_success(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        adapter.initialize()
        adapter.login(12345, "pass", "srv")
        assert adapter.is_authenticated

    def test_login_failure_raises(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = False
        adapter.initialize()
        with pytest.raises(AuthenticationError):
            adapter.login(12345, "wrong", "srv")

    def test_login_before_init_raises(self, mt5_mock, adapter):
        with pytest.raises(AdapterNotConnectedError):
            adapter.login(12345, "pass", "srv")


class TestLiveMT5AdapterShutdown:
    def test_shutdown_disconnects(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize()
        adapter.shutdown()
        assert not adapter.is_connected
        assert not adapter.is_authenticated
        mt5_mock.shutdown.assert_called_once()

    def test_shutdown_idempotent(self, mt5_mock, adapter):
        adapter.shutdown()
        assert not adapter.is_connected


class TestLiveMT5AdapterAccountInfo:
    def test_get_account_info(self, mt5_mock, adapter):
        mock_info = MagicMock()
        mock_info.balance = 10000.0
        mock_info.equity = 9500.0
        mock_info.margin = 500.0
        mock_info.margin_free = 9000.0
        mock_info.margin_level = 1900.0
        mock_info.currency = "USD"
        mock_info.name = "Test"
        mock_info.server = "Demo"
        mock_info.leverage = 100

        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        mt5_mock.account_info.return_value = mock_info
        adapter.initialize(login=1, password="p", server="s")
        info = adapter.get_account_info()
        assert info.balance == 10000.0

    def test_get_account_info_without_login(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            adapter.get_account_info()

    def test_get_account_info_none_raises(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        mt5_mock.account_info.return_value = None
        adapter.initialize(login=1, password="p", server="s")
        with pytest.raises(ConnectionError):
            adapter.get_account_info()


class TestLiveMT5AdapterData:
    def test_get_symbol_info_found(self, mt5_mock, adapter):
        mock_info = MagicMock()
        mock_info.digits = 5
        mock_info.spread = 10
        mock_info.currency_margin = "EUR"
        mock_info.trade_contract_size = 100000

        mt5_mock.initialize.return_value = True
        mt5_mock.symbol_info.return_value = mock_info
        adapter.initialize()
        info = adapter.get_symbol_info("EURUSD")
        assert info is not None
        assert info["digits"] == 5

    def test_get_symbol_info_not_found(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        mt5_mock.symbol_info.return_value = None
        adapter.initialize()
        info = adapter.get_symbol_info("UNKNOWN")
        assert info is None

    def test_get_rates(self, mt5_mock, adapter):
        mt5_mock.initialize.return_value = True
        mock_rates = [(1700000000, 1.1, 1.2, 1.0, 1.15, 100, 10, 100000)]
        mt5_mock.copy_rates_from_pos.return_value = mock_rates
        adapter.initialize()
        rates = adapter.get_rates("EURUSD", 1, 1)
        assert len(rates) == 1
        assert rates[0]["open"] == 1.1


class TestLiveMT5AdapterOrders:
    def test_send_order(self, mt5_mock, adapter):
        mock_result = MagicMock()
        mock_result.retcode = 10009
        mock_result.order = 1234
        mock_result.volume = 0.1
        mock_result.price = 1.1000
        mock_result.comment = "done"

        mt5_mock.TRADE_ACTION_DEAL = 1
        mt5_mock.TRADE_ACTION_PENDING = 5
        mt5_mock.ORDER_TYPE_BUY = 0
        mt5_mock.ORDER_TYPE_SELL = 1
        mt5_mock.ORDER_TIME_GTC = 0
        mt5_mock.ORDER_FILLING_IOC = 2
        mt5_mock.TRADE_RETCODE_DONE = 10009
        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        mt5_mock.order_send.return_value = mock_result

        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 0, 1.1000)
        assert result.ticket == 1234

    def test_get_positions(self, mt5_mock, adapter):
        mock_pos = MagicMock()
        mock_pos.ticket = 1
        mock_pos.symbol = "EURUSD"
        mock_pos.volume = 0.1
        mock_pos.type = 0
        mock_pos.price_open = 1.1000
        mock_pos.sl = 0.0
        mock_pos.tp = 0.0
        mock_pos.profit = 25.0
        mock_pos.swap = 0.0
        mock_pos.comment = ""

        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        mt5_mock.positions_get.return_value = [mock_pos]
        adapter.initialize(login=1, password="p", server="s")
        positions = adapter.get_positions()
        assert len(positions) == 1
        assert positions[0].symbol == "EURUSD"

    def test_get_orders(self, mt5_mock, adapter):
        mock_order = MagicMock()
        mock_order.ticket = 1
        mock_order.symbol = "EURUSD"
        mock_order.volume_initial = 0.1
        mock_order.type = 1
        mock_order.price_open = 1.2000
        mock_order.sl = 0.0
        mock_order.tp = 0.0

        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        mt5_mock.orders_get.return_value = [mock_order]
        adapter.initialize(login=1, password="p", server="s")
        orders = adapter.get_orders()
        assert len(orders) == 1

    def test_get_history_deals(self, mt5_mock, adapter):
        from datetime import datetime
        mock_deal = MagicMock()
        mock_deal.ticket = 1
        mock_deal.symbol = "EURUSD"
        mock_deal.volume = 0.1
        mock_deal.type = 0
        mock_deal.price = 1.1000
        mock_deal.profit = 50.0
        mock_deal.commission = -2.0
        mock_deal.swap = 0.0
        mock_deal.time = 1700000000
        mock_deal.time_close = 1700003600
        mock_deal.comment = ""

        mt5_mock.initialize.return_value = True
        mt5_mock.login.return_value = True
        adapter.initialize(login=1, password="p", server="s")
        now = datetime.now()
        mt5_mock.history_deals_get.return_value = [mock_deal]
        deals = adapter.get_history_deals(now, now)
        assert len(deals) == 1


class TestLiveMT5AdapterErrorHandling:
    def test_import_error_on_non_windows(self):
        from mt5.live import LiveMT5Adapter
        adapter = LiveMT5Adapter()
        adapter._mt5 = None
        with patch.object(
    adapter, "_import_mt5",
    side_effect=TerminalNotAvailableError("not available"),
):
            with pytest.raises(TerminalNotAvailableError):
                adapter.initialize()
