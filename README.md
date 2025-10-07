<div align="center">
  <h1>📅 Meeting Room Booking System</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/docker-ready-blue.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p>A Python console application to manage meeting room bookings in an office environment.</p>
</div>

---

## 🚀 Features

✔️ User management  
✔️ Meeting room management  
✔️ Booking creation with time slot validation (no overlaps)  
✔️ Booking deletion and filtering by date  
✔️ View bookings by user or room  
✔️ Data persistence using JSON files  
✔️ Validation for date formats and time ranges  
✔️ Modular architecture: models, services, repositories, patterns, utils  
✔️ Console-based interactive menu  
✔️ Docker-ready deployment  
✔️ Comprehensive unit tests for all core features

---

## 📁 Project Structure

```text
meet-room-booking/
├── src/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── data/
│   ├── patterns/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🧰 Requirements

- Python 3.11+
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

### 3️⃣ Ejecutar la aplicación

#### Modo consola (aplicación original):
```powershell
# Si usás entorno virtual en Windows:
& .\.venv\Scripts\Activate.ps1
python -m src.main

# O simplemente:
python -m src.main
```

#### Modo servidor web (con endpoint /health):
```powershell
# Si usás entorno virtual en Windows:
& .\.venv\Scripts\Activate.ps1
python run_web.py

# La aplicación estará disponible en:
# http://127.0.0.1:5000/health
```

#### Endpoint de salud:
El servidor web expone un endpoint de monitoreo en `GET /health` que devuelve:
```json
{
  "status": "ok", 
  "timestamp": "2025-10-02T10:30:00Z"
}
```

---

## 🐳 Docker Setup

To run the application in Docker:

### 1️⃣ Build the image
```bash
docker build -t meet-room-booking .
```

### 2️⃣ Run the container
```bash
# Modo web (default):
docker run -p 5000:5000 meet-room-booking
# Acceder a: http://localhost:5000/health

# Modo consola:
docker run -it meet-room-booking python -m src.main
```

---

## 🧪 Testing

Unit tests are located in the `tests/` directory and cover:
- Booking creation, deletion, and overlap prevention
- Room and user management
- Date and time validation

To run tests:
```bash
pytest
```
# Meet Room Booking

[![CI Pipeline](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml/badge.svg)](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/dario-coronel/meet-room-booking/branch/main/graph/badge.svg)](https://codecov.io/gh/dario-coronel/meet-room-booking)
---

## 📖 License

This project is licensed under the MIT License.
