from datetime import datetime, timedelta

import pytest

from src.utils.datetime_validator import (parse_datetime,
                                          validate_datetime_range,
                                          validate_not_in_past)


def test_parse_valid_datetime():
    dt = parse_datetime("2024-01-01 10:00")
    assert isinstance(dt, datetime)
    assert dt.year == 2024
    assert dt.hour == 10


def test_parse_invalid_datetime():
    with pytest.raises(ValueError) as excinfo:
        parse_datetime("01-01-2024 10:00")
    assert "invalid date format" in str(excinfo.value).lower()


def test_validate_datetime_range_valid():
    start = datetime(2024, 1, 1, 10, 0)
    end = datetime(2024, 1, 1, 11, 0)
    assert validate_datetime_range(start, end) is True


def test_validate_datetime_range_invalid():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 1, 11, 0)
    assert validate_datetime_range(start, end) is False


def test_validate_not_in_past_valid():
    future_time = datetime.now() + timedelta(hours=1)
    assert validate_not_in_past(future_time) is True


def test_validate_not_in_past_invalid():
    past_time = datetime.now() - timedelta(hours=1)
    assert validate_not_in_past(past_time) is False
