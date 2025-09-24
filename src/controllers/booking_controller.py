from flask import Blueprint, request, jsonify
from src.services.booking_service import BookingService
from src.services.room_service import RoomService
from src.services.user_service import UserService
from src.repositories.booking_repository import BookingRepository
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.patterns.no_overlap_strategy import NoOverlapStrategy

# Create blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize repositories
booking_repo = BookingRepository()
room_repo = RoomRepository()
user_repo = UserRepository()

# Initialize validator with concrete implementation
time_validator = NoOverlapStrategy()

# Initialize services with dependencies
booking_service = BookingService(booking_repo, time_validator)
room_service = RoomService(room_repo)
user_service = UserService(user_repo)


@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    """Get all available rooms."""
    try:
        rooms = room_service.get_all_rooms()
        return jsonify([{
            'id': room.room_id,
            'name': room.name,
            'capacity': room.capacity
        } for room in rooms]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users."""
    try:
        users = user_service.get_all_users()
        return jsonify([{
            'id': user.user_id,
            'name': user.name,
            'email': user.email
        } for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/bookings', methods=['POST'])
def create_booking():
    """Create a new booking."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'user_name', 'room_id', 'date', 'start_time', 'end_time'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing field: {field}'
                }), 400
        
        booking = booking_service.create_booking(
            data['user_name'],
            data['room_id'],
            data['date'],
            data['start_time'],
            data['end_time']
        )
        
        if booking:
            return jsonify({
                'id': booking.booking_id,
                'user_name': booking.user_name,
                'room_id': booking.room_id,
                'date': booking.date.isoformat(),
                'start_time': booking.start_time.isoformat(),
                'end_time': booking.end_time.isoformat()
            }), 201
        else:
            return jsonify({
                'error': 'Failed to create booking'
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/bookings', methods=['GET'])
def get_bookings():
    """Get all bookings or filter by user."""
    try:
        user_name = request.args.get('user_name')
        
        if user_name:
            bookings = booking_service.get_bookings_by_user(user_name)
        else:
            bookings = booking_service.get_all_bookings()
        
        return jsonify([{
            'id': booking.booking_id,
            'user_name': booking.user_name,
            'room_id': booking.room_id,
            'date': booking.date.isoformat(),
            'start_time': booking.start_time.isoformat(),
            'end_time': booking.end_time.isoformat()
        } for booking in bookings]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Delete a booking."""
    try:
        user_name = request.args.get('user_name')
        if not user_name:
            return jsonify({
                'error': 'user_name parameter required'
            }), 400
        
        success = booking_service.delete_booking(booking_id, user_name)
        
        if success:
            return jsonify({
                'message': 'Booking deleted successfully'
            }), 200
        else:
            return jsonify({
                'error': 'Booking not found or permission denied'
            }), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500