from datetime import datetime

def validate_datetime_range(start: datetime, end: datetime) -> bool:
    return start < end

def validate_not_in_past(start: datetime) -> bool:
    return start > datetime.now()

def parse_datetime(input_str: str) -> datetime:
    try:
        return datetime.strptime(input_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM.")