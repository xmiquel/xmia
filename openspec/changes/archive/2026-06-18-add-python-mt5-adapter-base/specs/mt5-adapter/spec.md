## ADDED Requirements

### Requirement: MT5Adapter Port Interface (Protocol)
The system SHALL provide a Protocol class MT5Adapter that defines the contract for all MT5 interactions. The interface SHALL include methods for: initialize, login, shutdown, get_account_info, get_symbol_info, get_rates, get_positions, get_orders, send_order, modify_order, modify_position, cancel_order, and get_history_deals. Domain code SHALL depend on this interface, never on concrete implementations.

#### Scenario: Interface defines all required methods
- **WHEN** inspecting the MT5Adapter Protocol class
- **THEN** it SHALL declare all required methods with proper signatures
- **AND** any class with matching method signatures SHALL conform to the Protocol automatically

#### Scenario: Domain code depends on interface
- **WHEN** domain logic receives an MT5Adapter instance
- **THEN** it SHALL only use methods defined on the MT5Adapter interface
- **AND** it SHALL NOT import MetaTrader5 directly

### Requirement: LiveMT5Adapter Implementation
The system SHALL provide a LiveMT5Adapter that wraps the MetaTrader5 native Python module. The adapter SHALL lazy-import MetaTrader5 on first use to avoid ImportError on non-Windows platforms. All MT5 interactions SHALL use the native module's functions and translate return codes into the custom exception hierarchy.

#### Scenario: Lazy import on non-Windows
- **WHEN** LiveMT5Adapter is instantiated on a non-Windows platform
- **THEN** the constructor SHALL not raise an error
- **AND** importing MetaTrader5 SHALL only occur when a connection method is called

#### Scenario: Live adapter translates MT5 return codes
- **WHEN** MetaTrader5 returns an error code from an operation
- **THEN** LiveMT5Adapter SHALL translate it into the appropriate custom exception

#### Scenario: Live adapter returns account info
- **WHEN** get_account_info() is called after successful login
- **THEN** it SHALL return an AccountInfo dataclass with balance, equity, margin, and currency

### Requirement: FakeMT5Adapter for Testing
The system SHALL provide a FakeMT5Adapter that implements the MT5Adapter interface using in-memory state. The fake adapter SHALL NOT require a live MT5 terminal. It SHALL support configurable responses (success, failure, timeout, specific error codes) to enable comprehensive testing.

#### Scenario: Fake adapter works without MT5
- **WHEN** FakeMT5Adapter is instantiated and used
- **THEN** it SHALL NOT attempt to import or interact with MetaTrader5
- **AND** all interface methods SHALL work with in-memory state

#### Scenario: Fake adapter supports success response
- **WHEN** a method is called in default happy-path mode
- **THEN** it SHALL return valid simulated data (mock account info, mock prices, etc.)

#### Scenario: Fake adapter supports error simulation
- **WHEN** configured for error mode for a specific operation
- **THEN** it SHALL raise the configured exception (e.g., AuthenticationError, ConnectionError)

#### Scenario: Contract tests pass with both adapters
- **WHEN** the same test suite is run against FakeMT5Adapter and LiveMT5Adapter
- **THEN** both adapters SHALL pass the same contract tests (live tests skipped if MT5 unavailable)

### Requirement: Account Information
The adapter SHALL provide account information including balance, equity, margin, free margin, margin level, and account currency. This SHALL be exposed as a typed data structure (AccountInfo dataclass).

#### Scenario: Get account info after login
- **WHEN** get_account_info() is called after successful authentication
- **THEN** it SHALL return an AccountInfo with all fields populated

#### Scenario: Get account info without login
- **WHEN** get_account_info() is called before login()
- **THEN** the adapter SHALL raise AdapterNotConnectedError

### Requirement: Market Data Access
The adapter SHALL provide access to symbol information and price data. get_symbol_info SHALL return symbol properties (digits, spread, margin requirements). get_rates SHALL return historical rates for a specified timeframe and count.

#### Scenario: Get symbol info for existing symbol
- **WHEN** get_symbol_info() is called with a valid symbol name
- **THEN** it SHALL return symbol metadata including digits, spread, and margin info

#### Scenario: Get symbol info for invalid symbol
- **WHEN** get_symbol_info() is called with an invalid symbol name
- **THEN** the adapter SHALL return None or raise a clear not-found error

#### Scenario: Get rates for symbol
- **WHEN** get_rates() is called with a valid symbol, timeframe, and count
- **THEN** it SHALL return a list of rate data (time, open, high, low, close, volume)

### Requirement: Order Operations
The adapter SHALL support sending, modifying, and canceling orders. send_order SHALL accept order parameters (symbol, volume, type, price, sl, tp). get_orders SHALL return pending orders. get_positions SHALL return open positions. modify_order SHALL modify a pending order. modify_position SHALL modify an open position's SL/TP. cancel_order SHALL cancel a pending order.

#### Scenario: Send market order
- **WHEN** send_order() is called with a market order request
- **THEN** the adapter SHALL execute the order
- **AND** return order result data (ticket number, filled volume, price)

#### Scenario: Get open positions
- **WHEN** get_positions() is called
- **THEN** the adapter SHALL return all currently open positions

#### Scenario: Get pending orders
- **WHEN** get_orders() is called
- **THEN** the adapter SHALL return all pending orders

#### Scenario: Modify pending order
- **WHEN** modify_order() is called with a valid ticket, price, sl, or tp
- **THEN** the adapter SHALL update the pending order parameters

#### Scenario: Modify open position
- **WHEN** modify_position() is called with a valid ticket, sl, or tp
- **THEN** the adapter SHALL update the open position's stop loss and take profit

#### Scenario: Cancel pending order
- **WHEN** cancel_order() is called with a valid ticket
- **THEN** the adapter SHALL remove the pending order

### Requirement: History Operations
The adapter SHALL provide access to closed deal history for strategy analysis. get_history_deals SHALL accept a date range and return all closed deals within that range.

#### Scenario: Get history deals within range
- **WHEN** get_history_deals() is called with a valid from_date and to_date
- **THEN** it SHALL return a list of closed deals (ticket, symbol, volume, profit, open/close time, etc.)

#### Scenario: Get history deals with invalid range
- **WHEN** get_history_deals() is called with from_date after to_date
- **THEN** the adapter SHALL raise a clear validation error
