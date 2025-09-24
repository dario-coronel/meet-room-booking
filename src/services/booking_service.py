from datetime import datetime

from src.models.booking import Booking
from src.patterns.time_validation_strategy import TimeValidationStrategy
from src.repositories.booking_repository import BookingRepository


class BookingService:
    def __init__(
        self, repository: BookingRepository, validator: TimeValidationStrategy
    ):
        self.repository = repository
        self.validator = validator

    def create_booking(self, room, user, start_time: datetime, end_time: datetime):
        # Create a temporary booking object (not yet added to repo)
        temp_booking = Booking(-1, room, user, start_time, end_time)
        existing_bookings = self.repository.get_by_room(room.room_id)

        if not self.validator.is_valid(temp_booking, existing_bookings):
            raise ValueError("Time slot overlaps with an existing booking.")

        # Now add it for real
        return self.repository.add(room, user, start_time, end_time)

    def get_bookings_by_user(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def get_bookings_by_room(self, room_id: int):
        return self.repository.get_by_room(room_id)

    def delete_booking(self, booking_id: int):
        return self.repository.delete(booking_id)

    def get_all_bookings(self):
        return self.repository.get_all()
