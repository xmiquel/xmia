class MT5Error(Exception):
    pass


class TerminalNotAvailableError(MT5Error):
    pass


class ConnectionError(MT5Error):
    pass


class AuthenticationError(MT5Error):
    pass


class AdapterNotConnectedError(MT5Error):
    pass
