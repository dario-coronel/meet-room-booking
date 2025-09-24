from datetime import datetime

from src.models.room import Room
from src.models.user import User
from src.patterns.no_overlap_strategy import NoOverlapStrategy
from src.repositories.booking_repository import BookingRepository
from src.services.booking_service import BookingService


def test_overlapping_booking():
    repo = BookingRepository(filepath="src/data/test_bookings.json")
    repo.bookings = []
    repo.next_id = 1

    room = Room(1, "Room A", 10, "Floor 1")
    user1 = User(1, "Alice", "alice@example.com")
    user2 = User(2, "Bob", "bob@example.com")

    service = BookingService(repo, NoOverlapStrategy())

    service.create_booking(
        room, user1, datetime(2025, 1, 1, 10, 0), datetime(2025, 1, 1, 11, 0)
    )

    try:
        service.create_booking(
            room, user2, datetime(2025, 1, 1, 10, 30), datetime(2025, 1, 1, 11, 30)
        )
        assert False, "Expected overlap error"
    except ValueError as e:
        assert "overlaps" in str(e).lower()
