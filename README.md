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
✔️ View bookings by user or room  
✔️ Modular architecture: models, services, repositories, patterns  
✔️ Console-based interactive menu  
✔️ Docker-ready deployment

---

## 📁 Project Structure

```text
meet-room-booking/
├── src/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── patterns/
│   └── main.py
├── test/
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

### 3️⃣ Run the application
```bash
python src/main.py
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
docker run -it meet-room-booking
```

---

## 🧪 Testing

Unit tests should be placed in the `test/` directory.

To run tests:
```bash
pytest
```

---

## 📖 License

This project is licensed under the MIT License.