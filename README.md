<div align="center">
  <h1>📅 Meeting Room Booking System</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/Flask-3.0%2B-green.svg" alt="Flask">
    <img src="https://img.shields.io/badge/Redis-7.0-red.svg" alt="Redis">
    <img src="https://img.shields.io/badge/docker-ready-blue.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p>Sistema completo de gestión de reservas de salas de reunión con modo consola interactivo y API REST con monitoreo en tiempo real.</p>
</div>

---

## ⚡ Redis Integration & Monitoring

La aplicación incluye integración completa con Redis para persistir y monitorear todas las peticiones a los endpoints de salud.

### Características de monitoreo:
- 🔍 **Persistencia automática**: Cada request a `/health` y `/ping` se guarda en Redis con metadata completa
- 📊 **Análisis de tráfico**: Endpoint `/get-responses` para consultar historial de requests
- 🎯 **Filtros avanzados**: Por endpoint específico y límite de resultados
- 📈 **Estadísticas en tiempo real**: Total de requests por endpoint
- 💾 **Datos almacenados**: IP, user-agent, timestamp y metadata adicional

---

## 🚀 Features

### Funcionalidades principales:
✔️ **Gestión completa**: Usuarios, salas de reunión y reservas  
✔️ **Validación inteligente**: Prevención de solapamientos y validación de horarios  
✔️ **API REST**: Endpoints `/health`, `/ping` y `/get-responses` para monitoreo  
✔️ **Persistencia dual**: JSON para datos de negocio, Redis para monitoreo  
✔️ **Arquitectura limpia**: Patrón Repository, Strategy y separación de responsabilidades  
✔️ **Modo dual**: Consola interactiva y servidor web Flask  
✔️ **Testing completo**: Cobertura de tests unitarios y de integración  
✔️ **Docker ready**: Docker Compose para despliegue con Redis incluido  
✔️ **CI/CD integrado**: Pipeline con GitHub Actions

---

## 📁 Project Structure

```text
meet-room-booking/
├── src/
│   ├── controllers/          # Flask controllers y endpoints
│   │   └── health_controller.py
│   ├── database/            # Cliente Redis y conexiones
│   │   └── redis_client.py
│   ├── models/              # Entidades del dominio
│   │   ├── booking.py
│   │   ├── room.py
│   │   └── user.py
│   ├── services/            # Lógica de negocio
│   │   ├── booking_service.py
│   │   ├── room_service.py
│   │   └── user_service.py
│   ├── repositories/        # Persistencia de datos
│   │   ├── booking_repository.py
│   │   ├── room_repository.py
│   │   └── user_repository.py
│   ├── patterns/            # Patrones de diseño
│   │   ├── no_overlap_strategy.py
│   │   └── time_validation_strategy.py
│   ├── utils/               # Utilidades
│   │   └── datetime_validator.py
│   ├── app.py              # Aplicación Flask principal
│   └── main.py             # Aplicación consola
├── tests/                   # Tests unitarios e integración
│   ├── test_health_endpoint.py
│   ├── test_redis_endpoints.py
│   └── ...
├── docker compose.yml       # Orquestación Docker
├── Dockerfile              # Imagen de la aplicación
├── run_web.py              # Entrypoint servidor web
├── requirements.txt        # Dependencias Python
└── README.md
```

---

## 🧰 Requirements

- Python 3.11+
- pip
- Docker & Docker Compose (opcional, para Redis y despliegue)
- Redis 7+ (si se ejecuta localmente sin Docker)

---

## ⚙️ Installation & Usage

### 🚀 Quick Start (Recomendado)

**La forma más rápida de ejecutar el proyecto completo:**

```bash
# 1. Clonar el repositorio
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking

# 2. Iniciar con Docker Compose (Redis + App)
docker compose up -d

# 3. Probar los endpoints
curl http://localhost:5000/health
curl http://localhost:5000/ping

# 4. Registrar un token para endpoints protegidos
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token-123"}'

# 5. Consultar requests guardados (requiere autenticación)
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer mi-token-123"
```

📖 **Para instrucciones detalladas de ejecución, consulta:** [EJECUCION.md](./EJECUCION.md)

### Otras opciones de ejecución

#### Modo consola (aplicación original de gestión de reservas):
```bash
python -m src.main
```

#### Modo servidor web local (sin Docker):
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar Redis (requiere Docker)
docker run -d -p 6379:6379 --name redis redis:7-alpine

# 3. Ejecutar la aplicación
python run_web.py
```

#### Endpoints disponibles:

##### Endpoints Públicos (sin autenticación):

**GET /health** - Health check endpoint
```json
{
  "status": "ok", 
  "timestamp": "2025-10-06T10:30:00Z"
}
```

**GET /ping** - Ping endpoint
```json
{
  "status": "pong",
  "timestamp": "2025-10-06T10:30:00Z",
  "message": "Service is alive"
}
```

**POST /register-token** - Registrar token para autenticación
```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "tu-token-aqui", "expiration_seconds": 3600}'
```

##### Endpoints Protegidos (requieren autenticación con Bearer token):

**GET /get-responses** - Obtener todos los requests guardados
```json
{
  "total_returned": 10,
  "redis_connected": true,
  "stats": {
    "connected": true,
    "total_requests": 25,
    "health_requests": 15,
    "ping_requests": 10
  },
  "requests": [
    {
      "endpoint": "/health",
      "ip_address": "127.0.0.1",
      "user_agent": "curl/7.68.0",
      "timestamp": "2025-10-06T10:30:00",
      "additional_data": {"response_status": "ok"}
    }
  ]
}
```

**Uso con autenticación:**
```bash
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer tu-token-aqui"
```

**Query parameters for /get-responses:**
- `limit` (default: 100): Maximum number of requests to return
- `endpoint`: Filter by specific endpoint (e.g., `/health` or `/ping`)

**DELETE /clear-responses** - Eliminar todos los requests guardados
```bash
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer tu-token-aqui"
```

---

## 🐳 Docker Compose Setup (Recommended)

Run the application with Redis using Docker Compose:

### 1️⃣ Start all services
```bash
docker compose up -d
```

This will start:
- Redis container on port 6379
- Application container on port 5000

### 2️⃣ Access the endpoints
```bash
# Health check
curl http://localhost:5000/health

# Ping
curl http://localhost:5000/ping

# Get all stored requests
curl http://localhost:5000/get-responses

# Get requests with limit
curl http://localhost:5000/get-responses?limit=10

# Get requests for specific endpoint
curl http://localhost:5000/get-responses?endpoint=/health
```

### 3️⃣ Stop services
```bash
docker compose down
```

### 4️⃣ View logs
```bash
docker compose logs -f app
docker compose logs -f redis
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

La suite de tests cubre funcionalidad completa del sistema:

### Tests disponibles:
- ✅ **test_booking_*.py**: Gestión de reservas y validaciones
- ✅ **test_room_service.py / test_user_service.py**: Servicios de salas y usuarios
- ✅ **test_health_endpoint.py**: Endpoint de salud (5 tests)
- ✅ **test_redis_endpoints.py**: Endpoints Redis y persistencia (9 tests)
- ✅ **test_datetime_validator.py**: Validaciones de fechas

### Ejecutar tests:
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_health_endpoint.py -v
pytest tests/test_redis_endpoints.py -v

# Con cobertura
pytest --cov=src --cov-report=html
```

### Resultados actuales:
- 📊 **20+ tests** pasando exitosamente
- ✅ Cobertura de endpoints críticos
- ✅ Validación de persistencia Redis
- ✅ Tests de performance (< 100ms)

---
## 📊 Arquitectura y Patrones

El proyecto implementa patrones de diseño y mejores prácticas:

### Patrones implementados:
- **Repository Pattern**: Abstracción de acceso a datos (JSON y Redis)
- **Strategy Pattern**: Validaciones intercambiables (`NoOverlapStrategy`, `TimeValidationStrategy`)
- **Factory Pattern**: Creación de app Flask en `health_controller.create_app()`
- **Dependency Injection**: Servicios reciben repositorios como dependencias

### Arquitectura:
```
┌─────────────────┐
│   Controllers   │ ← Flask endpoints (health, ping, get-responses)
└────────┬────────┘
         │
┌────────▼────────┐
│    Services     │ ← Lógica de negocio
└────────┬────────┘
         │
┌────────▼────────┐
│  Repositories   │ ← Persistencia (JSON + Redis)
└────────┬────────┘
         │
┌────────▼────────┐
│     Models      │ ← Entidades del dominio
└─────────────────┘
```

---

# Meet Room Booking

[![CI Pipeline](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml/badge.svg)](https://github.com/dario-coronel/meet-room-booking/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/dario-coronel/meet-room-booking/branch/main/graph/badge.svg)](https://codecov.io/gh/dario-coronel/meet-room-booking)
---

## 📖 License

This project is licensed under the MIT License.
