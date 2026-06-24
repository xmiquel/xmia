from unittest.mock import MagicMock, patch

import pytest


def pytest_addoption(parser):
    parser.addoption("--runlive", action="store_true", default=False, help="Run live MT5 tests")


@pytest.fixture
def runlive(request):
    if not request.config.getoption("--runlive"):
        pytest.skip("requires --runlive flag")


@pytest.fixture
def fake_adapter():
    from mt5.fake import FakeMT5Adapter

    return FakeMT5Adapter()


@pytest.fixture
def fake_adapter_no_terminal():
    from mt5.fake import FakeMT5Adapter

    return FakeMT5Adapter(simulate_terminal_available=False)


@pytest.fixture
def fake_adapter_authenticated(fake_adapter):
    fake_adapter.initialize(login=1, password="p", server="s")
    return fake_adapter


@pytest.fixture
def mt5_mock():
    with patch.dict("sys.modules", {"MetaTrader5": MagicMock()}) as _mock_modules:
        import MetaTrader5

        MetaTrader5.initialize.return_value = True
        MetaTrader5.login.return_value = True
        MetaTrader5.shutdown.return_value = True
        MetaTrader5.last_error.return_value = (0, "no error")
        MetaTrader5.account_info.return_value = None
        MetaTrader5.symbol_info.return_value = None
        MetaTrader5.copy_rates_from_pos.return_value = None
        MetaTrader5.positions_get.return_value = None
        MetaTrader5.orders_get.return_value = None
        MetaTrader5.order_send.return_value = None
        MetaTrader5.history_deals_get.return_value = None
        yield MetaTrader5


@pytest.fixture
def live_adapter():
    from mt5.live import LiveMT5Adapter

    return LiveMT5Adapter()


@pytest.fixture
def adapter(live_adapter):
    return live_adapter
