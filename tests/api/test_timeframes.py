import pytest
from api.timeframes import TIMEFRAMES, parse_timeframe


def test_all_timeframes_defined():
    expected = {
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
    assert TIMEFRAMES == expected


def test_parse_valid_timeframe():
    assert parse_timeframe("PERIOD_H1") == 16385


def test_parse_valid_timeframe_lowercase():
    assert parse_timeframe("period_h1") == 16385


def test_parse_invalid_timeframe():
    with pytest.raises(ValueError, match="Invalid timeframe"):
        parse_timeframe("INVALID")
