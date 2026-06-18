
import pytest

from mt5.errors import AdapterNotConnectedError
from mt5.fake import FakeMT5Adapter

pytestmark = [pytest.mark.live]


class BaseContractTest:
    adapter: FakeMT5Adapter

    def test_initialize_success(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        assert self.adapter.is_connected

    def test_initialize_twice(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        self.adapter.initialize()
        assert self.adapter.is_connected

    def test_shutdown_idempotent(self):
        self.adapter = self.make_adapter()
        self.adapter.shutdown()
        assert not self.adapter.is_connected

    def test_login_requires_init(self):
        self.adapter = self.make_adapter()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.login(1, "pass", "srv")

    def test_shutdown_disconnects(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        self.adapter.shutdown()
        assert not self.adapter.is_connected

    def test_get_account_info_requires_auth(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.get_account_info()

    def test_get_symbol_info_requires_init(self):
        self.adapter = self.make_adapter()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.get_symbol_info("EURUSD")

    def test_get_rates_requires_init(self):
        self.adapter = self.make_adapter()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.get_rates("EURUSD", 1, 10)

    def test_send_order_requires_auth(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.send_order("EURUSD", 0.1, 0, 1.1000)

    def test_get_positions_requires_auth(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.get_positions()

    def test_cancel_order_requires_auth(self):
        self.adapter = self.make_adapter()
        self.adapter.initialize()
        with pytest.raises(AdapterNotConnectedError):
            self.adapter.cancel_order(1)


class TestFakeContract(BaseContractTest):
    def make_adapter(self):
        return FakeMT5Adapter()


@pytest.mark.skip(reason="Live tests require MT5 terminal with MetaTrader5 package installed")
class TestLiveContract(BaseContractTest):
    def make_adapter(self):
        from mt5.live import LiveMT5Adapter
        return LiveMT5Adapter()
