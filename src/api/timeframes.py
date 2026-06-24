TIMEFRAMES: dict[str, int] = {
    "PERIOD_M1": 1,
    "PERIOD_M3": 3,
    "PERIOD_M5": 5,
    "PERIOD_M6": 6,
    "PERIOD_M12": 12,
    "PERIOD_M15": 15,
    "PERIOD_M24": 24,
    "PERIOD_M30": 30,
    "PERIOD_H1": 16385,
    "PERIOD_H4": 16388,
    "PERIOD_D1": 16408,
    "PERIOD_W1": 32769,
    "PERIOD_MN1": 49153,
}

VALID_TIMEFRAMES = list(TIMEFRAMES.keys())


def parse_timeframe(name: str) -> int:
    value = TIMEFRAMES.get(name.upper())
    if value is None:
        raise ValueError(
            f"Invalid timeframe '{name}'. Valid options: {', '.join(VALID_TIMEFRAMES)}"
        )
    return value
