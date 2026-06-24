import os

from pydantic import BaseModel, field_validator


class MT5Config(BaseModel):
    terminal_path: str | None = None
    account_number: int
    password: str
    server: str
    timeout: int = 30
    reconnect_attempts: int = 3
    reconnect_delay: int = 5

    @classmethod
    def from_env(cls) -> "MT5Config":
        return cls(
            terminal_path=os.getenv("MT5_PATH"),
            account_number=int(os.getenv("MT5_LOGIN", "0")),
            password=os.getenv("MT5_PASSWORD", ""),
            server=os.getenv("MT5_SERVER", ""),
            timeout=int(os.getenv("MT5_TIMEOUT", "30")),
            reconnect_attempts=int(os.getenv("MT5_RECONNECT_ATTEMPTS", "3")),
            reconnect_delay=int(os.getenv("MT5_RECONNECT_DELAY", "5")),
        )

    @field_validator("account_number")
    @classmethod
    def validate_account_number(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("account_number must be a positive integer")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("password must not be empty")
        return v

    @field_validator("server")
    @classmethod
    def validate_server(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("server must not be empty")
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("timeout must be a positive integer")
        return v

    @field_validator("reconnect_attempts")
    @classmethod
    def validate_reconnect_attempts(cls, v: int) -> int:
        if v < 0:
            raise ValueError("reconnect_attempts must be non-negative")
        return v

    @field_validator("reconnect_delay")
    @classmethod
    def validate_reconnect_delay(cls, v: int) -> int:
        if v < 0:
            raise ValueError("reconnect_delay must be non-negative")
        return v
