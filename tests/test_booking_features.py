from datetime import datetime
from src.models.room import Room
from src.models.user import User
from src.repositories.booking_repository import BookingRepository

def setup_repository():
    repo = BookingRepository(filepath="src/data/test_bookings.json")
    repo.bookings = []
    repo.next_id = 1
    return repo

def test_delete_booking():
    repo = setup_repository()
    room = Room(1, "Room A", 10, "Floor 1")
    user = User(1, "Alice", "alice@example.com")

    booking = repo.add(room, user, datetime(2025, 1, 1, 10, 0), datetime(2025, 1, 1, 11, 0))
    assert repo.get_by_id(booking.booking_id) is not None

    deleted = repo.delete(booking.booking_id)
    assert deleted is True
    assert repo.get_by_id(booking.booking_id) is None

def test_filter_bookings_by_date():
    repo = setup_repository()
    room = Room(1, "Room A", 10, "Floor 1")
    user = User(1, "Alice", "alice@example.com")

    repo.add(room, user, datetime(2025, 1, 1, 10, 0), datetime(2025, 1, 1, 11, 0))
    repo.add(room, user, datetime(2025, 1, 2, 12, 0), datetime(2025, 1, 2, 13, 0))

    target_date = datetime(2025, 1, 1).date()
    filtered = [b for b in repo.bookings if b.start_time.date() == target_date]

    assert len(filtered) == 1
    assert filtered[0].start_time.hour == 10