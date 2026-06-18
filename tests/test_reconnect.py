import pytest

from mt5.config import MT5Config
from mt5.errors import ConnectionError
from mt5.fake import FakeMT5Adapter
from mt5.reconnect import reconnect


class TestReconnect:
    def test_reconnect_success(self):
        adapter = FakeMT5Adapter()
        adapter.initialize(login=1, password="p", server="s")
        adapter.shutdown()
        config = MT5Config(
    account_number=1, password="p", server="s",
    reconnect_attempts=3, reconnect_delay=1,
)
        reconnect(adapter, config)
        assert adapter.is_authenticated

    def test_reconnect_with_path(self):
        adapter = FakeMT5Adapter()
        config = MT5Config(
            terminal_path="C:/MT5",
            account_number=1,
            password="p",
            server="s",
            reconnect_attempts=3,
            reconnect_delay=1,
        )
        reconnect(adapter, config)
        assert adapter.is_authenticated

    def test_reconnect_raises_after_all_attempts(self):
        adapter = FakeMT5Adapter(simulate_terminal_available=False)
        config = MT5Config(
    account_number=1, password="p", server="s",
    reconnect_attempts=2, reconnect_delay=1,
)
        with pytest.raises(ConnectionError):
            reconnect(adapter, config)

    def test_reconnect_from_disconnected(self):
        adapter = FakeMT5Adapter()
        config = MT5Config(
    account_number=1, password="p", server="s",
    reconnect_attempts=3, reconnect_delay=1,
)
        reconnect(adapter, config)
        assert adapter.is_authenticated
