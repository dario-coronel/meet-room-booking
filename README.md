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

## 🚀 Quick Start

### Prerequisitos
- Docker instalado ([Descargar Docker](https://www.docker.com/get-started))
- Docker Compose (incluido con Docker Desktop)

> 📚 **Para una guía completa de Docker**: Ver [DOCKER.md](DOCKER.md) con instrucciones detalladas, troubleshooting y FAQ.

### Ejecutar el proyecto en 3 pasos

La forma más rápida de ejecutar el proyecto es usando **Docker Compose**:

```bash
# 1. Clonar el repositorio
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking

# 2. Iniciar todos los servicios (Redis + Aplicación)
docker-compose up -d

# 3. Verificar que está funcionando
curl http://localhost:5000/health
```

¡Listo! ✅ La aplicación estará disponible en `http://localhost:5000` con Redis configurado automáticamente.

### Comandos útiles

```bash
# Ver logs de la aplicación
docker-compose logs -f app

# Ver logs de Redis
docker-compose logs -f redis

# Detener los servicios
docker-compose down

# Reiniciar con reconstrucción de imágenes
docker-compose up -d --build

# Verificar que todo está funcionando correctamente
./examples/test-docker-setup.sh
```

> 💡 **Nota**: Para más opciones de ejecución (modo consola, instalación local, etc.), consulta las secciones detalladas a continuación.
> 
> 🧪 **Testing**: Usa el script `./examples/test-docker-setup.sh` para verificar que el setup de Docker está correcto.

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
├── docker-compose.yml       # Orquestación Docker
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

#### Modo servidor web (con endpoint /health y Redis):
```powershell
# Primero, levanta Redis con Docker:
docker run -d -p 6379:6379 --name redis redis:7-alpine

# Luego, ejecuta la aplicación:
& .\.venv\Scripts\Activate.ps1
python run_web.py

# La aplicación estará disponible en:
# http://127.0.0.1:5000/health
# http://127.0.0.1:5000/ping
# http://127.0.0.1:5000/get-responses
```

#### Endpoints disponibles:

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

**GET /get-responses** - Get all stored requests
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

**Query parameters for /get-responses:**
- `limit` (default: 100): Maximum number of requests to return
- `endpoint`: Filter by specific endpoint (e.g., `/health` or `/ping`)

---

## 🐳 Docker Compose Setup (Recomendado) ⭐

**Esta es la forma más fácil y recomendada de ejecutar el proyecto**. Docker Compose levanta automáticamente Redis y la aplicación con una sola línea de comando.

> 📖 **Documentación completa**: Ver [DOCKER.md](DOCKER.md) para guía detallada con más ejemplos y troubleshooting.

### 1️⃣ Iniciar todos los servicios
```bash
# Iniciar en modo background (detached)
docker-compose up -d

# O ver los logs en tiempo real
docker-compose up
```

Esto iniciará:
- 🔴 **Redis**: Container en puerto 6379 con persistencia de datos
- 🐍 **Aplicación Flask**: Container en puerto 5000 conectado a Redis

### 2️⃣ Verificar que está funcionando
```bash
# Health check
curl http://localhost:5000/health

# Ping
curl http://localhost:5000/ping

# Get all stored requests
curl http://localhost:5000/get-responses

# Get requests con límite
curl http://localhost:5000/get-responses?limit=10

# Get requests por endpoint específico
curl http://localhost:5000/get-responses?endpoint=/health
```

### 3️⃣ Ver logs
```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs solo de la aplicación
docker-compose logs -f app

# Logs solo de Redis
docker-compose logs -f redis
```

### 4️⃣ Detener los servicios
```bash
# Detener los containers (mantiene volúmenes)
docker-compose down

# Detener y eliminar volúmenes (borra datos de Redis)
docker-compose down -v
```

### 5️⃣ Reconstruir después de cambios en el código
```bash
# Reconstruir imagen y reiniciar
docker-compose up -d --build
```

### Arquitectura de Docker Compose
```
┌─────────────────────────────┐
│   meet-room-app:5000        │
│   (Flask Application)        │
└──────────────┬──────────────┘
               │ REDIS_HOST=redis
               │ REDIS_PORT=6379
               ▼
┌─────────────────────────────┐
│   meet-room-redis:6379      │
│   (Redis Database)           │
│   📁 Volume: redis-data      │
└─────────────────────────────┘
```

### 🔧 Troubleshooting Docker Compose

**Problema: Puerto 5000 ya en uso**
```bash
# Cambiar el puerto en docker-compose.yml
# Modificar "5000:5000" a "8080:5000"
# Luego reiniciar
docker-compose down
docker-compose up -d
```

**Problema: Container no inicia correctamente**
```bash
# Ver logs detallados
docker-compose logs app

# Verificar estado de los containers
docker-compose ps

# Reiniciar servicios
docker-compose restart
```

**Problema: Cambios en el código no se reflejan**
```bash
# Reconstruir la imagen
docker-compose build --no-cache
docker-compose up -d
```

**Problema: Redis no conecta**
```bash
# Verificar que Redis está corriendo
docker-compose ps redis

# Verificar healthcheck
docker inspect meet-room-redis | grep Health -A 10

# Reiniciar solo Redis
docker-compose restart redis
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
