import pytest
from datetime import datetime

from src.models.room import Room
from src.models.user import User

from src.repositories.booking_repository import BookingRepository
from src.services.booking_service import BookingService
from src.patterns.no_overlap_strategy import NoOverlapStrategy

def test_valid_booking():
    room = Room(1, "Room A", 10, "Floor 1")
    user = User(1, "Alice", "alice@example.com")

    repo = BookingRepository()
    service = BookingService(repo, NoOverlapStrategy())

    start = datetime(2024, 1, 1, 10, 0)
    end = datetime(2024, 1, 1, 11, 0)

    booking = service.create_booking(room, user, start, end)

    assert booking is not None
    assert booking.start_time == start
    assert booking.end_time == end

def test_overlapping_booking():
    room = Room(1, "Room A", 10, "Floor 1")
    user1 = User(1, "Alice", "alice@example.com")
    user2 = User(2, "Bob", "bob@example.com")

    repo = BookingRepository()
    service = BookingService(repo, NoOverlapStrategy())

    # First booking: 10:00 - 11:00
    service.create_booking(room, user1, datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 11, 0))

    # Overlapping booking: 10:30 - 11:30
    with pytest.raises(ValueError) as excinfo:
        service.create_booking(room, user2, datetime(2024, 1, 1, 10, 30), datetime(2024, 1, 1, 11, 30))

    assert "overlaps" in str(excinfo.value).lower()