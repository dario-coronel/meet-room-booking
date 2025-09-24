<div align="center">
  <h1>📅 Meeting Room Booking System</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/flask-3.0%2B-green.svg" alt="Flask Version">
    <img src="https://img.shields.io/badge/docker-ready-blue.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/health--check-enabled-brightgreen.svg" alt="Health Check">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p>A Python web application to manage meeting room bookings with REST API and health monitoring.</p>
</div>

---

## 🚀 Features

✔️ **Health Check Endpoint**: GET `/health` for service monitoring (TP Requirement)  
✔️ **REST API**: Complete booking management via HTTP endpoints  
✔️ **User Management**: Create and manage users via API  
✔️ **Meeting Room Management**: Room availability and capacity tracking  
✔️ **Booking System**: Create, view, and delete bookings with overlap prevention  
✔️ **Data Persistence**: JSON-based storage system  
✔️ **Interactive Console**: Optional command-line interface for development  
✔️ **Docker Ready**: Containerized deployment with port 5000  
✔️ **CI/CD Pipeline**: Automated testing including health endpoint validation  
✔️ **Comprehensive Tests**: Unit tests for all features + health endpoint compliance

---

## 🏗️ Project Structure

```text
meet-room-booking/
├── src/
│   ├── controllers/          # Web controllers (Flask routes)
│   │   ├── health_controller.py     # Health endpoint (TP requirement)
│   │   └── booking_controller.py    # Booking API endpoints
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   ├── repositories/        # Data access layer
│   ├── patterns/            # Design patterns
│   ├── utils/               # Utility functions
│   ├── data/                # JSON data storage
│   ├── app.py               # Main Flask application
│   └── main.py              # Console interface (optional)
├── tests/                   # Unit and integration tests
│   ├── test_health_endpoint.py      # Health endpoint tests (TP requirement)
│   └── ...                          # Other test files
├── .github/workflows/       # CI/CD pipeline
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
└── README.md               # This file
```

---

## 🔧 API Endpoints

### Health Check (TP Requirement)
- **GET** `/health` - Service health status
  ```json
  {
    "status": "ok",
    "timestamp": "2025-09-24T10:30:00Z"
  }
  ```

### Booking Management API
- **GET** `/api/rooms` - Get all available rooms
- **GET** `/api/users` - Get all users  
- **POST** `/api/bookings` - Create a new booking
- **GET** `/api/bookings` - Get all bookings (optional: `?user_name=xyz`)
- **DELETE** `/api/bookings/{id}` - Delete a booking

---

## 🧰 Requirements

- Python 3.11+
- Flask 3.0+
- pip

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/meet-room-booking.git
cd meet-room-booking
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the web application
```bash
python src/app.py
```

### 4️⃣ Access the application
- Health check: http://localhost:5000/health
- API endpoints: http://localhost:5000/api/

---

## 🐳 Docker Setup

### 1️⃣ Build the image
```bash
docker build -t meet-room-booking .
```

### 2️⃣ Run the container
```bash
docker run -p 5000:5000 meet-room-booking
```

### 3️⃣ Test the health endpoint
```bash
curl http://localhost:5000/health
```

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
# Unit tests only
pytest tests/test_*_service.py -v

# Health endpoint tests (TP requirement)
pytest tests/test_health_endpoint.py -v
```

---

## 📊 Health Check (TP Compliance)

The `/health` endpoint provides:
- **Status Code**: 200 (OK)  
- **Response Time**: < 100ms
- **JSON Response**: Valid JSON with required structure
- **No Authentication**: Public endpoint access
- **No External Dependencies**: Self-contained health check
- **Automated Testing**: CI pipeline validates endpoint

---

## 🔄 CI/CD Pipeline

The project includes automated:
- **Code Quality**: Black, isort, flake8, pylint
- **Unit Tests**: pytest with coverage reporting
- **Health Endpoint Validation**: Dedicated CI job testing TP requirements  
- **Docker Build**: Container verification
- **Integration Summary**: All pipeline results

---

## 🛠️ Development

### Code Quality
Pre-commit hooks ensure code quality:
```bash
python -m pre_commit install
```

### Console Mode (Development)
For development/testing, you can still use the console interface:
```bash
python src/main.py
```

---

## 📋 TP Requirements Compliance

✅ **Health Endpoint**: GET `/health` returns 200 status  
✅ **JSON Response**: Valid JSON with `"status": "ok"`  
✅ **Response Time**: < 100ms response time  
✅ **No Authentication**: Public endpoint access  
✅ **No External Dependencies**: Self-contained health check  
✅ **Automated Tests**: Comprehensive test suite in CI pipeline  
✅ **CI Pipeline Validation**: Dedicated job validates endpoint behavior

---

Ready for production deployment! 🎉
# Meet Room Booking

[![CI Pipeline](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml/badge.svg)](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/dario-coronel/meet-room-booking/branch/main/graph/badge.svg)](https://codecov.io/gh/dario-coronel/meet-room-booking)
---

## 📖 License

This project is licensed under the MIT License.
