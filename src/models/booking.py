from datetime import datetime

from src.models.room import Room
from src.models.user import User


class Booking:
    def __init__(
        self,
        booking_id: int,
        room: Room,
        user: User,
        start_time: datetime,
        end_time: datetime,
    ):
        self.booking_id = booking_id
        self.room = room
        self.user = user
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (
            f"Booking #{self.booking_id} - Room: {self.room.name}, "
            f"User: {self.user.name}, {self.start_time} → {self.end_time}"
        )
