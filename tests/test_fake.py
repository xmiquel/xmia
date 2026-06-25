from datetime import datetime, timedelta

import pytest

from mt5.errors import AdapterNotConnectedError, AuthenticationError, TerminalNotAvailableError
from mt5.fake import FakeMT5Adapter


class TestFakeMT5AdapterLifecycle:
    def test_initial_state(self):
        adapter = FakeMT5Adapter()
        assert not adapter.is_connected
        assert not adapter.is_authenticated

    def test_initialize_sets_connected(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        assert adapter.is_connected
        assert not adapter.is_authenticated

    def test_initialize_with_credentials_authenticates(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=123, password="secret", server="s")
        assert adapter.is_authenticated

    def test_initialize_without_terminal_raises(self):
        adapter = FakeMT5Adapter(simulate_terminal_available=False)
        with pytest.raises(TerminalNotAvailableError):
            adapter.initialize()

    def test_login_authenticates(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        adapter.login(login=123, password="secret", server="s")
        assert adapter.is_authenticated

    def test_login_wrong_password_raises(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        with pytest.raises(AuthenticationError):
            adapter.login(login=123, password="wrong", server="s")

    def test_login_before_init_raises(self):
        adapter = FakeMT5Adapter()
        with pytest.raises(AdapterNotConnectedError):
            adapter.login(login=123, password="secret", server="s")

    def test_shutdown_disconnects(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        adapter.shutdown()
        assert not adapter.is_connected
        assert not adapter.is_authenticated

    def test_shutdown_idempotent(self):
        adapter = FakeMT5Adapter()
        adapter.shutdown()
        assert not adapter.is_connected


class TestFakeMT5AdapterData:
    def test_get_account_info(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        info = adapter.get_account_info()
        assert info.balance == 10000.0
        assert info.currency == "USD"

    def test_get_account_info_without_login_raises(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            adapter.get_account_info()

    def test_get_symbol_info_known(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        info = adapter.get_symbol_info("EURUSD")
        assert info is not None
        assert info["digits"] == 5

    def test_get_symbol_info_unknown(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        info = adapter.get_symbol_info("UNKNOWN")
        assert info is None

    def test_get_symbol_info_case_insensitive(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        info = adapter.get_symbol_info("eurusd")
        assert info is not None

    def test_get_rates_returns_count(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        rates = adapter.get_rates("EURUSD", 1, 10)
        assert len(rates) == 10

    def test_get_rates_has_required_fields(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        rates = adapter.get_rates("EURUSD", 1, 1)
        r = rates[0]
        assert "time" in r
        assert "open" in r
        assert "high" in r
        assert "low" in r
        assert "close" in r
        assert "tick_volume" in r
        assert "spread" in r
        assert "real_volume" in r

    def test_get_rates_before_returns_count(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        before = int(datetime.now().timestamp()) + 100000
        rates = adapter.get_rates_before("EURUSD", 1, 10, before)
        assert len(rates) == 10

    def test_get_rates_before_all_before_timestamp(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        before = int(datetime.now().timestamp()) + 100000
        rates = adapter.get_rates_before("EURUSD", 1, 10, before)
        for r in rates:
            assert r["time"] < before

    def test_get_rates_before_filters_recent(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        before = int(datetime.now().timestamp()) - 1000
        rates = adapter.get_rates_before("EURUSD", 1, 10, before)
        for r in rates:
            assert r["time"] < before

    def test_get_rates_before_has_required_fields(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        before = int(datetime.now().timestamp()) + 100000
        rates = adapter.get_rates_before("EURUSD", 1, 1, before)
        r = rates[0]
        assert "time" in r
        assert "open" in r
        assert "high" in r
        assert "low" in r
        assert "close" in r
        assert "tick_volume" in r
        assert "spread" in r
        assert "real_volume" in r

    def test_get_rates_before_requires_state(self):
        adapter = FakeMT5Adapter()
        with pytest.raises(AdapterNotConnectedError):
            adapter.get_rates_before("EURUSD", 1, 1, 1000000)

    def test_get_rates_before_error_mode(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        adapter.set_error_mode("get_rates_before", ConnectionError)
        with pytest.raises(ConnectionError):
            adapter.get_rates_before("EURUSD", 1, 1, 1000000)


class TestFakeMT5AdapterOrders:
    def test_send_market_order_creates_position(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 0, 1.1000)
        assert result.ticket > 0
        assert result.filled_volume == 0.1
        positions = adapter.get_positions()
        assert len(positions) == 1
        assert positions[0].ticket == result.ticket

    def test_send_pending_order_creates_order(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 1, 1.2000)
        orders = adapter.get_orders()
        assert len(orders) == 1
        assert orders[0]["ticket"] == result.ticket

    def test_modify_order_updates_fields(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 1, 1.2000)
        adapter.modify_order(result.ticket, 1.2500, 1.1000, 1.3000)
        orders = adapter.get_orders()
        assert orders[0]["price"] == 1.2500
        assert orders[0]["sl"] == 1.1000

    def test_modify_order_not_found_raises(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        with pytest.raises(ValueError, match="not found"):
            adapter.modify_order(999, 1.2, 1.1, 1.3)

    def test_modify_position_updates_sl_tp(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 0, 1.1000)
        adapter.modify_position(result.ticket, 1.0500, 1.2000)
        positions = adapter.get_positions()
        assert positions[0].sl == 1.0500
        assert positions[0].tp == 1.2000

    def test_cancel_order_removes_it(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        result = adapter.send_order("EURUSD", 0.1, 1, 1.2000)
        adapter.cancel_order(result.ticket)
        assert len(adapter.get_orders()) == 0

    def test_get_positions_empty_initially(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        assert adapter.get_positions() == []

    def test_get_orders_empty_initially(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        assert adapter.get_orders() == []


class TestFakeMT5AdapterErrorSimulation:
    def test_error_mode_for_initialize(self):
        adapter = FakeMT5Adapter()
        adapter.set_error_mode("initialize", ConnectionError)
        with pytest.raises(ConnectionError):
            adapter.initialize()

    def test_error_mode_for_login(self):
        adapter = FakeMT5Adapter()
        adapter.initialize()
        adapter.set_error_mode("login", AuthenticationError)
        with pytest.raises(AuthenticationError):
            adapter.login(1, "p", "s")

    def test_error_mode_for_get_account_info(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        adapter.set_error_mode("get_account_info", ConnectionError)
        with pytest.raises(ConnectionError):
            adapter.get_account_info()

    def test_error_mode_disabled_after_set_to_none(self):
        adapter = FakeMT5Adapter()
        adapter.set_error_mode("initialize", ConnectionError)
        adapter.set_error_mode("initialize", None)
        adapter.initialize()
        assert adapter.is_connected


class TestFakeMT5AdapterNoMT5:
    def test_no_mt5_import_required(self):
        from mt5.fake import FakeMT5Adapter
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        info = adapter.get_account_info()
        assert info.balance == 10000.0


class TestFakeMT5AdapterHistory:
    def test_get_history_deals_empty_initially(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        now = datetime.now()
        deals = adapter.get_history_deals(now - timedelta(days=1), now)
        assert deals == []

    def test_get_history_deals_validates_dates(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        now = datetime.now()
        with pytest.raises(ValueError, match="from_date must be before to_date"):
            adapter.get_history_deals(now, now - timedelta(days=1))
