## 1. Project Setup

- [x] 1.1 Create src/mt5/ package with __init__.py
- [x] 1.2 Add pyproject.toml with project metadata and all tooling configs (ruff, bandit, mypy, pytest, coverage)
- [x] 1.3 Create .pre-commit-config.yaml with hooks for ruff, mypy, and bandit
- [x] 1.4 Create conftest.py with pytest fixtures for FakeMT5Adapter and LiveMT5Adapter

## 2. Error Handling

- [x] 2.1 Define MT5Error base exception class in errors.py
- [x] 2.2 Define TerminalNotAvailableError, ConnectionError, AuthenticationError, AdapterNotConnectedError
- [x] 2.3 Write tests verifying each exception can be raised and caught independently

## 3. Configuration Model (Pydantic)

- [x] 3.1 Implement MT5Config Pydantic model with fields and defaults: terminal_path, account_number, password, server, timeout, reconnect_attempts, reconnect_delay
- [x] 3.2 Implement from_env() classmethod for environment variable loading (MT5_*)
- [x] 3.3 Write tests: construction, defaults, Pydantic validation rules, env var loading, constructor precedence

## 4. Port Interface (MT5Adapter Protocol)

- [x] 4.1 Define MT5Adapter Protocol in protocol.py: initialize, login, shutdown, get_account_info, get_symbol_info, get_rates, get_positions, get_orders, send_order, modify_order, modify_position, cancel_order, get_history_deals
- [x] 4.2 Define shared types: AccountInfo, OrderResult, DealInfo, PositionInfo dataclasses
- [x] 4.3 Write interface conformance tests verifying Protocol structural typing

## 5. Fake Adapter (FakeMT5Adapter)

- [x] 5.1 Implement FakeMT5Adapter in fake.py with in-memory state
- [x] 5.2 Implement all 13 interface methods returning simulated data
- [x] 5.3 Add configurable error simulation per operation
- [x] 5.4 Track connection and authentication state (DISCONNECTED → INITIALIZED → AUTHENTICATED)
- [x] 5.5 Write tests verifying all FakeMT5Adapter methods work without MetaTrader5 import

## 6. Live Adapter (LiveMT5Adapter)

- [x] 6.1 Implement LiveMT5Adapter in live.py with lazy MetaTrader5 import
- [x] 6.2 Implement initialize() wrapping mt5.initialize() with optional login credentials
- [x] 6.3 Implement login() wrapping mt5.login() for re-authentication
- [x] 6.4 Implement shutdown() wrapping mt5.shutdown() as idempotent
- [x] 6.5 Implement get_account_info(), get_symbol_info(), get_rates() wrapping MT5 functions
- [x] 6.6 Implement get_positions(), get_orders(), send_order(), modify_order(), modify_position(), cancel_order(), get_history_deals() wrapping MT5 functions
- [x] 6.7 Translate all MT5 return codes into custom exceptions
- [x] 6.8 Add graceful ImportError handling on non-Windows platforms
- [x] 6.9 Write tests with mock for MetaTrader5 module

## 7. Connection Lifecycle

- [x] 7.1 Implement explicit initialize() with validation, error handling, and optional credentials for unified init+login
- [x] 7.2 Implement explicit shutdown() as idempotent operation
- [x] 7.3 Implement reconnect logic with configurable retry attempts and delay
- [x] 7.4 Track connection/authentication state within the adapter (DISCONNECTED → INITIALIZED → AUTHENTICATED)
- [x] 7.5 Write tests: init sequences, init+login combined, shutdown sequences, error states, reconnect behavior

## 8. Contract Tests and Integration

- [x] 8.1 Write shared contract test suite that validates behavioral parity across both adapters
- [x] 8.2 Add pytest markers (@pytest.mark.live) for tests requiring MT5 terminal
- [x] 8.3 Add pytest.skipif conditions for live tests when MT5 is unavailable
- [x] 8.4 Verify all unit tests pass without MT5 terminal
- [x] 8.5 Run full test suite and confirm zero failures in unit-test mode

## Tooling Commands Reference

```bash
# Run all quality checks
ruff check src/ tests/
bandit -r src/
mypy src/
pytest --cov=src --cov-report=term-missing

# Install pre-commit hooks (one-time setup)
pre-commit install
```
