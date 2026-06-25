## ADDED Requirements

### Requirement: List Visible Symbols

The system SHALL provide a method on the MT5 adapter to retrieve the list of symbol names visible in the terminal's Market Watch. Only symbols with `visible == True` SHALL be returned. The live adapter SHALL use `mt5.symbols_get()` and filter by the `visible` attribute. The fake adapter SHALL return a representative set of known symbols.

#### Scenario: Returns visible symbols from live adapter

- **GIVEN** the adapter is connected to MT5 with visible symbols in Market Watch
- **WHEN** `get_symbols()` is called
- **THEN** it SHALL return a list of symbol name strings
- **AND** all returned symbols SHALL have `visible == True` in MT5

#### Scenario: Fake adapter returns known symbols

- **GIVEN** the FakeMT5Adapter is initialized
- **WHEN** `get_symbols()` is called
- **THEN** it SHALL return a list of known symbol strings (e.g., EURUSD, GBPUSD, BTCUSD, AUDUSD, USDJPY)

#### Scenario: Adapter not connected raises error

- **GIVEN** the adapter is in an uninitialized or disconnected state
- **WHEN** `get_symbols()` is called
- **THEN** the adapter SHALL raise `AdapterNotConnectedError`
