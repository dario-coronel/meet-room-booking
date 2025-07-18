import json
import os
from datetime import datetime
from src.models.booking import Booking
from src.models.room import Room
from src.models.user import User

class BookingRepository:
    def __init__(self, filepath="src/data/bookings.json"):
        self.filepath = filepath
        self.bookings = []
        self.next_id = 1
        self.load_from_file()

    def add(self, room: Room, user: User, start_time: datetime, end_time: datetime) -> Booking:
        booking = Booking(self.next_id, room, user, start_time, end_time)
        self.bookings.append(booking)
        self.next_id += 1
        self.save_to_file()
        return booking

    def get_by_id(self, booking_id: int) -> Booking:
        return next((b for b in self.bookings if b.booking_id == booking_id), None)

    def get_by_user(self, user_id: int) -> list:
        return [b for b in self.bookings if b.user.user_id == user_id]

    def get_by_room(self, room_id: int) -> list:
        return [b for b in self.bookings if b.room.room_id == room_id]

    def delete(self, booking_id: int) -> bool:
        booking = self.get_by_id(booking_id)
        if booking:
            self.bookings.remove(booking)
            self.save_to_file()
            return True
        return False

    def load_from_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
                self.bookings = [
                    Booking(
                        booking_id=b["booking_id"],
                        room=Room(**b["room"]),
                        user=User(**b["user"]),
                        start_time=datetime.fromisoformat(b["start_time"]),
                        end_time=datetime.fromisoformat(b["end_time"])
                    )
                    for b in data
                ]
                if self.bookings:
                    self.next_id = max(b.booking_id for b in self.bookings) + 1

    def save_to_file(self):
        with open(self.filepath, "w") as f:
            json.dump([
                {
                    "booking_id": b.booking_id,
                    "room": b.room.__dict__,
                    "user": b.user.__dict__,
                    "start_time": b.start_time.isoformat(),
                    "end_time": b.end_time.isoformat()
                }
                for b in self.bookings
            ], f, indent=2)