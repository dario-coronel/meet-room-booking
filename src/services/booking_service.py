from src.repositories.booking_repository import BookingRepository
from src.patterns.time_validation_strategy import TimeValidationStrategy

class BookingService:
    def __init__(self, repository: BookingRepository, validator: TimeValidationStrategy):
        self.repository = repository
        self.validator = validator

    def create_booking(self, room, user, start_time, end_time):
        new_booking = self.repository.add(room, user, start_time, end_time)
        existing_bookings = self.repository.get_by_room(room.room_id)

        if not self.validator.is_valid(new_booking, existing_bookings):
            self.repository.delete(new_booking.booking_id)
            raise ValueError("Time slot overlaps with an existing booking.")

        return new_booking

    def get_bookings_by_user(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def get_bookings_by_room(self, room_id: int):
        return self.repository.get_by_room(room_id)

    def delete_booking(self, booking_id: int):
        return self.repository.delete(booking_id)