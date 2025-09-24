from datetime import datetime

from src.models.booking import Booking
from src.models.room import Room
from src.models.user import User
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.services.booking_service import BookingService
from src.services.room_service import RoomService
from src.services.user_service import UserService
from src.utils.datetime_validator import (
    parse_datetime,
    validate_datetime_range,
    validate_not_in_past,
)


def print_menu():
    print("\n=== Meeting Room Booking System ===")
    print("1. Create user")
    print("2. List users")
    print("3. Create room")
    print("4. List rooms")
    print("5. Make booking")
    print("6. List bookings")
    print("7. Cancel booking")
    print("8. Exit")


def create_user(user_service):
    print("\n--- Create User ---")
    name = input("Enter name: ")
    email = input("Enter email: ")
    
    try:
        user = user_service.create_user(name, email)
        print(f"User created successfully: {user}")
    except ValueError as e:
        print(f"Error: {e}")


def list_users(user_service):
    print("\n--- Users List ---")
    users = user_service.get_all_users()
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")


def create_room(room_service):
    print("\n--- Create Room ---")
    name = input("Enter room name: ")
    capacity = input("Enter capacity: ")
    
    try:
        capacity = int(capacity)
        room = room_service.create_room(name, capacity)
        print(f"Room created successfully: {room}")
    except ValueError as e:
        print(f"Error: {e}")


def list_rooms(room_service):
    print("\n--- Rooms List ---")
    rooms = room_service.get_all_rooms()
    if not rooms:
        print("No rooms found.")
    else:
        for room in rooms:
            print(
                f"ID: {room.id}, Name: {room.name}, "
                f"Capacity: {room.capacity}"
            )


def make_booking(booking_service, user_service, room_service):
    print("\n--- Make Booking ---")
    
    # Show available users
    users = user_service.get_all_users()
    if not users:
        print("No users available. Create a user first.")
        return
    
    print("Available users:")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}")
    
    # Show available rooms
    rooms = room_service.get_all_rooms()
    if not rooms:
        print("No rooms available. Create a room first.")
        return
    
    print("\nAvailable rooms:")
    for room in rooms:
        print(f"ID: {room.id}, Name: {room.name}")
    
    try:
        user_id = int(input("\nEnter user ID: "))
        room_id = int(input("Enter room ID: "))
        start_time_str = input("Enter start time (YYYY-MM-DD HH:MM): ")
        end_time_str = input("Enter end time (YYYY-MM-DD HH:MM): ")
        
        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)
        
        validate_not_in_past(start_time)
        validate_datetime_range(start_time, end_time)
        
        booking = booking_service.create_booking(
            user_id, room_id, start_time, end_time
        )
        print(f"Booking created successfully: {booking}")
        
    except ValueError as e:
        print(f"Error: {e}")


def list_bookings(booking_service):
    print("\n--- Bookings List ---")
    bookings = booking_service.get_all_bookings()
    if not bookings:
        print("No bookings found.")
    else:
        for booking in bookings:
            print(
                f"ID: {booking.id}, User: {booking.user_id}, "
                f"Room: {booking.room_id}, "
                f"Start: {booking.start_time}, End: {booking.end_time}"
            )


def cancel_booking(booking_service):
    print("\n--- Cancel Booking ---")
    
    # Show current bookings
    bookings = booking_service.get_all_bookings()
    if not bookings:
        print("No bookings found.")
        return
    
    print("Current bookings:")
    for booking in bookings:
        print(
            f"ID: {booking.id}, User: {booking.user_id}, "
            f"Room: {booking.room_id}, "
            f"Start: {booking.start_time}, End: {booking.end_time}"
        )
    
    try:
        booking_id = int(input("\nEnter booking ID to cancel: "))
        booking_service.cancel_booking(booking_id)
        print("Booking cancelled successfully!")
        
    except ValueError as e:
        print(f"Error: {e}")


def main():
    # Initialize repositories
    user_repository = UserRepository()
    room_repository = RoomRepository()
    
    # Initialize services
    user_service = UserService(user_repository)
    room_service = RoomService(room_repository)
    booking_service = BookingService(
        user_repository, room_repository
    )
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            create_user(user_service)
        elif choice == "2":
            list_users(user_service)
        elif choice == "3":
            create_room(room_service)
        elif choice == "4":
            list_rooms(room_service)
        elif choice == "5":
            make_booking(booking_service, user_service, room_service)
        elif choice == "6":
            list_bookings(booking_service)
        elif choice == "7":
            cancel_booking(booking_service)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
