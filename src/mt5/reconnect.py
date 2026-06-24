import time

from mt5.config import MT5Config
from mt5.errors import ConnectionError
from mt5.protocol import MT5Adapter


def reconnect(adapter: MT5Adapter, config: MT5Config) -> None:
    last_error: Exception | None = None
    for attempt in range(config.reconnect_attempts):
        try:
            adapter.shutdown()
            adapter.initialize(
                path=config.terminal_path,
                login=config.account_number,
                password=config.password,
                server=config.server,
                portable=config.portable,
            )
            return
        except Exception as e:
            last_error = e
            if attempt < config.reconnect_attempts - 1:
                time.sleep(config.reconnect_delay)

    raise ConnectionError(
        f"Reconnection failed after {config.reconnect_attempts} attempt(s): {last_error}"
    ) from last_error
