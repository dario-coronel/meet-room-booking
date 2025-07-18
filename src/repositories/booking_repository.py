from src.models.booking import Booking
from datetime import datetime

class BookingRepository:
    def __init__(self):
        self.bookings = []
        self.next_id = 1

    def add(self, room, user, start_time: datetime, end_time: datetime) -> Booking:
        booking = Booking(self.next_id, room, user, start_time, end_time)
        self.bookings.append(booking)
        self.next_id += 1
        return booking

    def get_by_id(self, booking_id: int) -> Booking:
        return next((b for b in self.bookings if b.booking_id == booking_id), None)

    def get_all(self) -> list:
        return self.bookings

    def get_by_user(self, user_id: int) -> list:
        return [b for b in self.bookings if b.user.user_id == user_id]

    def get_by_room(self, room_id: int) -> list:
        return [b for b in self.bookings if b.room.room_id == room_id]

    def delete(self, booking_id: int) -> bool:
        booking = self.get_by_id(booking_id)
        if booking:
            self.bookings.remove(booking)
            return True
        return False