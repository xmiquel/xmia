## Context

The project needs a clean, testable integration layer for MetaTrader 5 (MT5). Currently there is no Python package structure, no abstractions, and no testing strategy for MT5 interaction. MT5's native Python module (MetaTrader5) is a thin C++ bridge that requires a live MT5 terminal on Windows -- making code that calls it directly untestable in CI and non-Windows environments.

This design establishes a Port/Adapter (Hexagonal) architecture for the MT5 integration layer, with clear separation between the domain-facing interface (port) and the MT5-specific implementation (adapter). A fake adapter provides testability without a live terminal.

## Goals / Non-Goals

**Goals:**
- Define a stable port interface (MT5Adapter Protocol) that domain code depends on
- Implement LiveMT5Adapter wrapping the MetaTrader5 native module
- Implement FakeMT5Adapter for tests without a live terminal
- Provide configuration model for terminal path, credentials, and timeouts (Pydantic)
- Manage connection lifecycle (initialize, login, shutdown, reconnect)
- Graceful handling when MT5 is not installed or on non-Windows platforms

**Non-Goals:**
- High-level trading strategies or signal generation
- Database persistence of market data or orders
- REST API or web service layer (future changes)
- Docker containerization of the MT5 adapter

## Decisions

### 1. Port/Adapter Pattern (Hexagonal Architecture)

- **Decision**: Define MT5Adapter as a Protocol class using `typing.Protocol`. LiveMT5Adapter and FakeMT5Adapter both conform to it without needing explicit inheritance.
- **Rationale**: Domain code should never import MetaTrader5 directly. The port interface decouples business logic from the MT5 dependency, enabling testing, swapping implementations, and graceful degradation. Protocol provides structural subtyping -- any class with the right methods conforms automatically, no inheritance required.
- **Alternatives considered**: ABC (tight coupling via inheritance), simple duck-typing (no interface enforcement), direct coupling (untestable).

### 2. Package Structure

- **Decision**: Single `src/mt5/` package with separated responsibilities:
  - `protocol.py` -- MT5Adapter Protocol + shared types (AccountInfo, OrderResult, etc.)
  - `live.py` -- LiveMT5Adapter (wraps MetaTrader5 module, lazy import)
  - `fake.py` -- FakeMT5Adapter (in-memory state for tests)
  - `config.py` -- MT5Config model (Pydantic-based)
  - `errors.py` -- Custom exception hierarchy
- **Rationale**: Separating the protocol from the live adapter avoids accidental import of MetaTrader5 when only types are needed. The protocol file has zero external dependencies. Keeps each file focused on one responsibility.

### 3. Connection Lifecycle

- **Decision**: Explicit `initialize()` and `shutdown()` methods. `initialize()` accepts optional login credentials -- if provided, performs both init and authentication in one call. Connection state tracked internally via a 3-state model: `DISCONNECTED → INITIALIZED → AUTHENTICATED`. `shutdown()` is idempotent from any state.
- **Rationale**: MT5 terminal is a shared Windows process -- implicit connect/disconnect on every call is expensive and fragile. Explicit lifecycle gives callers control. Unifying credentials in `initialize()` matches MT5's native API where `mt5.initialize()` accepts optional login params, making the common case simpler.
- **Reconnect**: Retry wrapper with configurable attempts and delay (from MT5Config). Handles transient terminal/network errors.

### 4. Error Handling

- **Decision**: Custom exception hierarchy rooted in `MT5Error`. Categories: `ConnectionError`, `AuthenticationError`, `TerminalNotAvailableError`, `AdapterNotConnectedError`.
- **Rationale**: Callers need to distinguish between transient MT5 errors, auth failures, and terminal-not-installed conditions without parsing the native module's return codes.

### 5. Configuration Model

- **Decision**: Pydantic-based config model (`BaseModel`, mit `model_config = ConfigDict(env_prefix="MT5_")`). Fields: `terminal_path: str | None = None`, `account_number: int`, `password: str`, `server: str`, `timeout: int = 30`, `reconnect_attempts: int = 3`, `reconnect_delay: int = 5`.
- **Rationale**: Pydantic provides built-in validation (types, ranges, empty strings), automatic environment variable loading, and clear error messages -- all essential for a configuration that must not fail silently at runtime.
- **Alternatives considered**: Dataclass (simpler but no validation, no env loading), YAML file (extra dependency, parsing overhead).

### 6. Port Interface Scope

- **Decision**: The MT5Adapter Protocol includes methods for connection lifecycle, account info, market data, order operations, position management, and history retrieval. Specific methods:
  - `initialize(path, login, password, server)` -- init terminal with optional auth
  - `login(login, password, server)` -- (re)authenticate
  - `shutdown()` -- idempotent disconnect
  - `get_account_info()` -- balance, equity, margin, currency
  - `get_symbol_info(symbol)` -- digits, spread, margin
  - `get_rates(symbol, timeframe, count)` -- historical candles
  - `get_positions()` -- open positions
  - `get_orders()` -- pending orders
  - `send_order(symbol, volume, type, price, sl, tp)` -- place order
  - `modify_order(ticket, price, sl, tp)` -- modify pending order
  - `modify_position(ticket, sl, tp)` -- modify open position
  - `cancel_order(ticket)` -- cancel pending order
  - `get_history_deals(from_date, to_date)` -- closed deal history for strategy analysis
- **Rationale**: Covers the full range needed for trading strategies while staying focused. YAGNI applied -- added only what's justified by use cases.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| MT5 terminal not installed on dev machine | Cannot run integration tests | Fake adapter for unit tests; skip live tests with pytest.skipif |
| MetaTrader5 module fails to import on non-Windows | ImportError crashes application | Lazy import with graceful fallback; adapter raises TerminalNotAvailableError |
| MT5 terminal crashes or is busy | Connection failures cascade | Reconnect retry logic; configurable attempts and delay |
| Interface too broad in first iteration | Hard to change later | Protocol-based (structural) -- adding methods is backward compatible |
| Live adapter diverges from fake adapter behavior | Tests pass but prod fails | Shared contract test suite runs against both adapters to verify behavioral parity |

## Testing Strategy

- **Unit tests**: FakeMT5Adapter drives all adapter-interface unit tests without MT5
- **Contract tests**: Same test suite runs against both FakeMT5Adapter and LiveMT5Adapter (live tests skipped if MT5 unavailable)
- **Config tests**: Unit tests for Pydantic model validation and env-var loading
- **Connection tests**: Test initialize/shutdown sequences, error states, reconnect behavior
- **Platform tests**: Verify graceful ImportError handling on non-Windows (via mock)

## Migration Plan

1. Create `src/mt5/` package with `__init__.py`, `errors.py`, `config.py` (Pydantic model)
2. Implement `MT5Adapter` Protocol interface in `protocol.py`
3. Implement `FakeMT5Adapter` in `fake.py`
4. Write contract tests that run against both adapters
5. Implement `LiveMT5Adapter` in `live.py` (lazy MetaTrader5 import)
6. Add pytest markers and skip conditions for live tests
7. Verify all tests pass: unit tests always, live tests when MT5 available

## Open Questions

- Should config load from env vars only, or also `.env` file? Start with env vars only (Pydantic's `env_prefix`). `.env` support can be added via `python-dotenv` later if needed.
- Should the adapter expose async methods? Not for v1 -- MT5 Python module is synchronous. Async wrappers can be added later.
