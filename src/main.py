from datetime import datetime
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.repositories.booking_repository import BookingRepository

from src.services.room_service import RoomService
from src.services.user_service import UserService
from src.services.booking_service import BookingService

from src.patterns.no_overlap_strategy import NoOverlapStrategy

def print_menu():
    print("\n=== Meeting Room Booking System ===")
    print("1. Create user")
    print("2. Create room")
    print("3. Make a booking")
    print("4. View bookings by user")
    print("5. View bookings by room")
    print("6. Exit")

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
            try:
                user_id = int(input("Enter user ID: "))
                room_id = int(input("Enter room ID: "))
                start_str = input("Enter start time (YYYY-MM-DD HH:MM): ")
                end_str = input("Enter end time (YYYY-MM-DD HH:MM): ")

                user = user_repo.get_by_id(user_id)
                room = room_repo.get_by_id(room_id)

                if not user or not room:
                    print("Invalid user or room ID.")
                    continue

                start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")

                booking = booking_service.create_booking(room, user, start_time, end_time)
                print(f"Booking created: {booking}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            user_id = int(input("Enter user ID: "))
            bookings = booking_service.get_bookings_by_user(user_id)
            for b in bookings:
                print(b)

        elif choice == "5":
            room_id = int(input("Enter room ID: "))
            bookings = booking_service.get_bookings_by_room(room_id)
            for b in bookings:
                print(b)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()