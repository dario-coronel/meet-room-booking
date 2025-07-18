# Meeting Room Booking System

This is a Python-based console application designed to manage meeting room bookings in an office environment. It follows Object-Oriented Programming principles and implements the Strategy Design Pattern to validate booking time slots.

---

## 🚀 Features

- Create and manage users
- Create and manage meeting rooms
- Make bookings with time slot validation (no overlapping)
- View bookings by user or by room
- Modular architecture with models, services, repositories, and patterns
- Console-based interactive menu
- Ready for Docker deployment

---

## 📁 Project Structure
meeting-room-booking/ 
├── src/ │   
├── models/ 
│   ├── services/ 
│   ├── repositories/ 
│   ├── patterns/ 
│   └── main.py 
├── tests/ 
├── requirements.txt 
├── Dockerfile 
└── README.md


---

## 🧰 Requirements

- Python 3.11+
- pip (Python package manager)

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/meeting-room-booking.git
   cd meeting-room-booking

2. Install dependencies:

pip install -r requirements.txt

3. Run the application:

python src/main.py

🐳 Docker Setup (Optional)To run the application inside a Docker container:

1.  Build the image:

docker build -t meeting-room-booking 

2.  Run the container:

docker run -it meeting-room-booking


🧪 Testing

Unit tests will be located in the tests/ directory. To run tests:

python -m unittest discover tests