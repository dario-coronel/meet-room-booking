class Room:
    def __init__(self, room_id: int, name: str, capacity: int, location: str):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.location = location

    def __str__(self):
        return f"Room {self.name} (Capacity: {self.capacity}, Location: {self.location})"