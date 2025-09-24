from src.patterns.time_validation_strategy import TimeValidationStrategy


class NoOverlapStrategy(TimeValidationStrategy):
    def is_valid(self, new_booking, existing_bookings) -> bool:
        for booking in existing_bookings:
            if booking.room.room_id != new_booking.room.room_id:
                continue
            if (
                new_booking.start_time < booking.end_time
                and new_booking.end_time > booking.start_time
            ):
                return False
        return True
