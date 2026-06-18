import os

import pytest

from mt5.config import MT5Config


class TestMT5Config:
    def test_create_with_all_fields(self):
        config = MT5Config(
            terminal_path="C:/Program Files/MetaTrader 5",
            account_number=123456,
            password="secret",
            server="ICMarkets-Demo",
            timeout=60,
            reconnect_attempts=5,
            reconnect_delay=10,
        )
        assert config.terminal_path == "C:/Program Files/MetaTrader 5"
        assert config.account_number == 123456
        assert config.password == "secret"
        assert config.server == "ICMarkets-Demo"
        assert config.timeout == 60
        assert config.reconnect_attempts == 5
        assert config.reconnect_delay == 10

    def test_create_with_defaults(self):
        config = MT5Config(
            account_number=123456,
            password="secret",
            server="ICMarkets-Demo",
        )
        assert config.terminal_path is None
        assert config.timeout == 30
        assert config.reconnect_attempts == 3
        assert config.reconnect_delay == 5

    def test_validate_account_number_positive(self):
        with pytest.raises(ValueError, match="account_number must be a positive integer"):
            MT5Config(account_number=0, password="secret", server="s")

        with pytest.raises(ValueError, match="account_number must be a positive integer"):
            MT5Config(account_number=-1, password="secret", server="s")

    def test_validate_password_not_empty(self):
        with pytest.raises(ValueError, match="password must not be empty"):
            MT5Config(account_number=1, password="", server="s")

        with pytest.raises(ValueError, match="password must not be empty"):
            MT5Config(account_number=1, password="   ", server="s")

    def test_validate_server_not_empty(self):
        with pytest.raises(ValueError, match="server must not be empty"):
            MT5Config(account_number=1, password="secret", server="")

    def test_validate_timeout_positive(self):
        with pytest.raises(ValueError, match="timeout must be a positive integer"):
            MT5Config(account_number=1, password="secret", server="s", timeout=0)

        with pytest.raises(ValueError, match="timeout must be a positive integer"):
            MT5Config(account_number=1, password="secret", server="s", timeout=-5)

    def test_validate_reconnect_attempts_non_negative(self):
        with pytest.raises(ValueError, match="reconnect_attempts must be non-negative"):
            MT5Config(account_number=1, password="secret", server="s", reconnect_attempts=-1)

    def test_validate_reconnect_delay_non_negative(self):
        with pytest.raises(ValueError, match="reconnect_delay must be non-negative"):
            MT5Config(account_number=1, password="secret", server="s", reconnect_delay=-1)

    def test_env_var_loading(self):
        os.environ["MT5_ACCOUNT_NUMBER"] = "98765"
        os.environ["MT5_PASSWORD"] = "envpass"
        os.environ["MT5_SERVER"] = "EnvServer-Demo"
        os.environ["MT5_TIMEOUT"] = "45"

        config = MT5Config.from_env()

        assert config.account_number == 98765
        assert config.password == "envpass"
        assert config.server == "EnvServer-Demo"
        assert config.timeout == 45

        del os.environ["MT5_ACCOUNT_NUMBER"]
        del os.environ["MT5_PASSWORD"]
        del os.environ["MT5_SERVER"]
        del os.environ["MT5_TIMEOUT"]

    def test_constructor_overrides_env(self):
        os.environ["MT5_ACCOUNT_NUMBER"] = "99999"

        config = MT5Config(account_number=11111, password="secret", server="s")

        assert config.account_number == 11111

        del os.environ["MT5_ACCOUNT_NUMBER"]
