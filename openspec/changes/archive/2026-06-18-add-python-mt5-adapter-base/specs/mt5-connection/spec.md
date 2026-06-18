## ADDED Requirements

### Requirement: Initialize MT5 Terminal
The adapter SHALL initialize the MetaTrader 5 terminal with a configured path. If no path is provided, the adapter SHALL use the default MT5 installation path. Initialize SHALL accept optional login credentials (login, password, server) — if provided, SHALL perform authentication as part of initialization. Initialization MUST happen before any trading or data operations.

#### Scenario: Successful initialization
- **WHEN** initialize() is called with a valid terminal path
- **THEN** the adapter SHALL return a success indicator
- **AND** the adapter SHALL be in a connected state

#### Scenario: Initialize with default path
- **WHEN** initialize() is called without specifying a terminal path
- **THEN** the adapter SHALL use the default MT5 installation path

#### Scenario: Initialize with invalid path
- **WHEN** initialize() is called with an invalid or non-existent terminal path
- **THEN** the adapter SHALL raise TerminalNotAvailableError
- **AND** the adapter SHALL remain in a disconnected state

#### Scenario: Initialize with credentials
- **WHEN** initialize() is called with valid credentials (login, password, server)
- **THEN** the adapter SHALL initialize the terminal AND authenticate
- **AND** the adapter SHALL be in an authenticated state

### Requirement: Login to Trading Account
The adapter SHALL authenticate with an MT5 trading account using the configured credentials (account number, password, server). Login MUST fail with a clear error if credentials are invalid or the server is unreachable. This method is available for re-authentication without re-initializing the terminal.

#### Scenario: Successful login
- **WHEN** login() is called with valid credentials after initialization
- **THEN** the adapter SHALL return account information
- **AND** the adapter SHALL be in an authenticated state

#### Scenario: Login with invalid credentials
- **WHEN** login() is called with invalid account number or password
- **THEN** the adapter SHALL raise AuthenticationError
- **AND** the adapter SHALL remain unauthenticated

#### Scenario: Login before initialization
- **WHEN** login() is called before initialize()
- **THEN** the adapter SHALL raise AdapterNotConnectedError

### Requirement: Shutdown Terminal
The adapter SHALL gracefully disconnect from the MT5 terminal and release all resources on shutdown. After shutdown, the adapter MUST NOT allow any further operations.

#### Scenario: Successful shutdown
- **WHEN** shutdown() is called while connected
- **THEN** the adapter SHALL disconnect from the terminal
- **AND** the adapter SHALL release all resources
- **AND** the adapter SHALL be in a disconnected state

#### Scenario: Shutdown when not connected
- **WHEN** shutdown() is called while already disconnected
- **THEN** the adapter SHALL not raise an error (idempotent)

### Requirement: Reconnect Handling
The adapter SHALL support reconnection with configurable retry attempts and delay between attempts. Reconnection SHALL attempt to re-initialize and re-login using the original configuration.

#### Scenario: Successful reconnection
- **WHEN** the connection is lost and reconnect is triggered
- **THEN** the adapter SHALL retry up to the configured number of attempts
- **AND** the adapter SHALL wait the configured delay between attempts
- **AND** if successful, the adapter SHALL return to authenticated state

#### Scenario: Reconnection fails after all attempts
- **WHEN** all reconnection attempts fail
- **THEN** the adapter SHALL raise ConnectionError
- **AND** the adapter SHALL remain in a disconnected state
