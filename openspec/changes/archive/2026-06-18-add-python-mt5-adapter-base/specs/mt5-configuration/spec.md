## ADDED Requirements

### Requirement: Configuration Model
The system SHALL provide a Pydantic configuration model (MT5Config) that holds all connection parameters. Fields SHALL include: terminal_path (Optional[str], default None), account_number (int), password (str), server (str), timeout (int, default 30), reconnect_attempts (int, default 3), reconnect_delay (int, default 5). All fields SHALL have sensible defaults where applicable.

#### Scenario: Create config with all fields
- **WHEN** MT5Config is created with all parameters specified
- **THEN** all fields SHALL contain the provided values

#### Scenario: Create config with defaults
- **WHEN** MT5Config is created with only required fields (account_number, password, server)
- **THEN** terminal_path SHALL default to None
- **AND** timeout SHALL default to 30
- **AND** reconnect_attempts SHALL default to 3
- **AND** reconnect_delay SHALL default to 5

### Requirement: Environment Variable Loading
The configuration model SHALL support loading values from environment variables. The model SHALL use Pydantic's ConfigDict with env_prefix="MT5_". Environment variable names: MT5_TERMINAL_PATH, MT5_ACCOUNT_NUMBER, MT5_PASSWORD, MT5_SERVER, MT5_TIMEOUT. Explicit constructor arguments SHALL take precedence over environment variables.

#### Scenario: Load from environment
- **WHEN** MT5Config() is called with no arguments and environment variables are set
- **THEN** it SHALL read values from MT5_* environment variables
- **AND** return a fully populated config instance

#### Scenario: Constructor overrides environment
- **WHEN** MT5Config is constructed with an explicit account_number and MT5_ACCOUNT_NUMBER is also set
- **THEN** the explicit constructor argument SHALL take precedence

### Requirement: Validation on Construction
The configuration model SHALL validate parameters on construction via Pydantic's built-in validation. Validation SHALL ensure: account_number is a positive integer, password is not empty, server is not empty, timeout is a positive integer, reconnect_attempts is non-negative, reconnect_delay is non-negative.

#### Scenario: Validates account number
- **WHEN** MT5Config is created with a non-positive account_number
- **THEN** it SHALL raise a validation error

#### Scenario: Validates password not empty
- **WHEN** MT5Config is created with an empty password
- **THEN** it SHALL raise a validation error

#### Scenario: Validates timeout positive
- **WHEN** MT5Config is created with a negative timeout
- **THEN** it SHALL raise a validation error
