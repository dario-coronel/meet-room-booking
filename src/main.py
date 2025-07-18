from datetime import datetime
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.repositories.booking_repository import BookingRepository

from src.services.room_service import RoomService
from src.services.user_service import UserService
from src.services.booking_service import BookingService

from src.patterns.no_overlap_strategy import NoOverlapStrategy
from src.utils.datetime_validator import (
    parse_datetime,
    validate_datetime_range,
    validate_not_in_past
)

def print_menu():
    print("\n=== Meeting Room Booking System ===")
    print("1. Create user")
    print("2. Create room")
    print("3. Make a booking")
    print("4. View bookings by user")
    print("5. View bookings by room")
    print("6. List all users and rooms")
    print("7. Delete a booking")
    print("8. View bookings by date")
    print("9. Exit")

def main():
    room_repo = RoomRepository()
    user_repo = UserRepository()
    booking_repo = BookingRepository()

    room_service = RoomService(room_repo)
    user_service = UserService(user_repo)
    booking_service = BookingService(booking_repo, NoOverlapStrategy())

    while True:
        print_menu()
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            user = user_service.create_user(name, email)
            print(f"User created: {user}")

        elif choice == "2":
            name = input("Enter room name: ")
            capacity = int(input("Enter room capacity: "))
            location = input("Enter room location: ")
            room = room_service.create_room(name, capacity, location)
            print(f"Room created: {room}")

        elif choice == "3":
            users = user_service.get_all_users()
            rooms = room_service.get_all_rooms()

            if not users:
                print("No users available. Please create a user first.")
                continue
            if not rooms:
                print("No rooms available. Please create a room first.")
                continue

            print("\nAvailable Users:")
            for user in users:
                print(f"ID: {user.user_id} - {user.name} ({user.email})")

            print("\nAvailable Rooms:")
            for room in rooms:
                print(f"ID: {room.room_id} - {room.name} (Capacity: {room.capacity}, Location: {room.location})")

            try:
                user_id = int(input("\nEnter user ID: "))
                room_id = int(input("Enter room ID: "))
                start_str = input("Enter start time (YYYY-MM-DD HH:MM): ")
                end_str = input("Enter end time (YYYY-MM-DD HH:MM): ")

                user = user_repo.get_by_id(user_id)
                room = room_repo.get_by_id(room_id)

                if not user or not room:
                    print("Invalid user or room ID.")
                    continue

                start_time = parse_datetime(start_str)
                end_time = parse_datetime(end_str)

                if not validate_datetime_range(start_time, end_time):
                    print("❌ Start time must be before end time.")
                    continue

                if not validate_not_in_past(start_time):
                    print("❌ Start time must be in the future.")
                    continue

                booking = booking_service.create_booking(room, user, start_time, end_time)
                print(f"\n✅ Booking created:\n{booking}")
            except Exception as e:
                print(f"\n❌ Error: {e}")

        elif choice == "4":
            users = user_service.get_all_users()
            if not users:
                print("No users available.")
                continue

            print("\nAvailable Users:")
            for user in users:
                print(f"ID: {user.user_id} - {user.name} ({user.email})")

            user_id = int(input("\nEnter user ID to view bookings: "))
            bookings = booking_service.get_bookings_by_user(user_id)
            if bookings:
                for b in bookings:
                    print(b)
            else:
                print("No bookings found for this user.")

        elif choice == "5":
            rooms = room_service.get_all_rooms()
            if not rooms:
                print("No rooms available.")
                continue

            print("\nAvailable Rooms:")
            for room in rooms:
                print(f"ID: {room.room_id} - {room.name} (Capacity: {room.capacity}, Location: {room.location})")

            room_id = int(input("\nEnter room ID to view bookings: "))
            bookings = booking_service.get_bookings_by_room(room_id)
            if bookings:
                for b in bookings:
                    print(b)
            else:
                print("No bookings found for this room.")

        elif choice == "6":
            users = user_service.get_all_users()
            rooms = room_service.get_all_rooms()

            print("\n=== Users ===")
            if users:
                for user in users:
                    print(f"ID: {user.user_id} - {user.name} ({user.email})")
            else:
                print("No users available.")

            print("\n=== Rooms ===")
            if rooms:
                for room in rooms:
                    print(f"ID: {room.room_id} - {room.name} (Capacity: {room.capacity}, Location: {room.location})")
            else:
                print("No rooms available.")

        elif choice == "7":
            bookings = booking_repo.bookings
            if not bookings:
                print("No bookings available.")
                continue

            print("\n=== Existing Bookings ===")
            for b in bookings:
                print(f"ID: {b.booking_id} - Room: {b.room.name}, User: {b.user.name}, {b.start_time} → {b.end_time}")

            try:
                booking_id = int(input("\nEnter booking ID to delete: "))
                booking = booking_repo.get_by_id(booking_id)
                if not booking:
                    print("❌ Booking not found.")
                    continue

                confirm = input(f"Are you sure you want to delete booking #{booking_id}? (y/n): ").lower()
                if confirm == "y":
                    deleted = booking_service.delete_booking(booking_id)
                    print("✅ Booking deleted.")
                else:
                    print("❌ Deletion cancelled.")
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "8":
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                bookings = [
                    b for b in booking_repo.bookings
                    if b.start_time.date() == target_date
                ]
                if bookings:
                    print(f"\nBookings on {target_date}:")
                    for b in bookings:
                        print(f"ID: {b.booking_id} - Room: {b.room.name}, User: {b.user.name}, {b.start_time} → {b.end_time}")
                else:
                    print("No bookings found on that date.")
            except ValueError:
                print("❌ Invalid date format.")

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()