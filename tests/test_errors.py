import pytest

from mt5.errors import (
    AdapterNotConnectedError,
    AuthenticationError,
    ConnectionError,
    MT5Error,
    TerminalNotAvailableError,
)


class TestMT5Errors:
    def test_mt5_error_is_base(self):
        assert issubclass(TerminalNotAvailableError, MT5Error)
        assert issubclass(ConnectionError, MT5Error)
        assert issubclass(AuthenticationError, MT5Error)
        assert issubclass(AdapterNotConnectedError, MT5Error)

    def test_terminal_not_available(self):
        with pytest.raises(TerminalNotAvailableError):
            raise TerminalNotAvailableError("MT5 not found")

    def test_connection_error(self):
        with pytest.raises(ConnectionError):
            raise ConnectionError("Connection failed")

    def test_authentication_error(self):
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Invalid credentials")

    def test_adapter_not_connected(self):
        with pytest.raises(AdapterNotConnectedError):
            raise AdapterNotConnectedError("Not connected")

    def test_each_caught_independently(self):
        errors = [
            TerminalNotAvailableError,
            ConnectionError,
            AuthenticationError,
            AdapterNotConnectedError,
        ]
        for err_type in errors:
            try:
                raise err_type("test")
            except MT5Error:
                pass
            except Exception:
                pytest.fail(f"{err_type.__name__} should be caught by MT5Error")

    def test_error_message(self):
        msg = "custom message"
        err = TerminalNotAvailableError(msg)
        assert str(err) == msg
