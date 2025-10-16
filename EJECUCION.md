# 🚀 Guía de Ejecución del Proyecto

Esta guía te ayudará a ejecutar el proyecto Meeting Room Booking System paso a paso.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Opción 1: Ejecución con Docker Compose (Recomendado)](#opción-1-ejecución-con-docker-compose-recomendado)
3. [Opción 2: Ejecución Local con Redis en Docker](#opción-2-ejecución-local-con-redis-en-docker)
4. [Opción 3: Solo Aplicación (Sin Redis)](#opción-3-solo-aplicación-sin-redis)
5. [Uso de la API](#uso-de-la-api)
6. [Autenticación con Tokens](#autenticación-con-tokens)
7. [Pruebas Automatizadas](#pruebas-automatizadas)

---

## Requisitos Previos

### Opción Docker (Recomendado):
- Docker Desktop instalado y en ejecución
- Docker Compose

### Opción Local:
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Docker (solo para Redis)

---

## Opción 1: Ejecución con Docker Compose (Recomendado)

Esta es la forma más sencilla de ejecutar el proyecto completo con Redis.

### Paso 1: Clonar el repositorio (si aún no lo has hecho)

```bash
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking
```

### Paso 2: Iniciar los servicios

```bash
docker-compose up -d
```

Este comando iniciará:
- **Redis** en el puerto `6379`
- **Aplicación Flask** en el puerto `5000`

### Paso 3: Verificar que los servicios estén corriendo

```bash
docker-compose ps
```

Deberías ver algo como:

```
NAME                IMAGE               STATUS              PORTS
meet-room-app       meet-room-booking   Up 10 seconds       0.0.0.0:5000->5000/tcp
meet-room-redis     redis:7-alpine      Up 10 seconds       0.0.0.0:6379->6379/tcp
```

### Paso 4: Ver los logs de la aplicación

```bash
docker-compose logs -f app
```

### Paso 5: Probar los endpoints

**Endpoint de salud (sin autenticación):**
```bash
curl http://localhost:5000/health
```

**Endpoint de ping (sin autenticación):**
```bash
curl http://localhost:5000/ping
```

### Paso 6: Detener los servicios

```bash
docker-compose down
```

---

## Opción 2: Ejecución Local con Redis en Docker

Si prefieres ejecutar la aplicación localmente pero usar Redis en Docker.

### Paso 1: Iniciar Redis en Docker

```bash
docker run -d -p 6379:6379 --name meet-room-redis redis:7-alpine
```

### Paso 2: Crear un entorno virtual de Python (recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

**En Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación

```bash
python run_web.py
```

Verás un mensaje como:
```
Starting Flask web server...
Health endpoint available at: http://127.0.0.1:5000/health
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

### Paso 5: Probar los endpoints

Abre otra terminal y ejecuta:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/ping
```

### Paso 6: Detener Redis cuando termines

```bash
docker stop meet-room-redis
docker rm meet-room-redis
```

---

## Opción 3: Solo Aplicación (Sin Redis)

Puedes ejecutar la aplicación sin Redis, pero las funciones de persistencia no estarán disponibles.

### Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar la aplicación

```bash
python run_web.py
```

**Nota:** Verás un mensaje de advertencia:
```
Warning: Redis not available: Error 111 connecting to localhost:6379
```

Esto es normal y la aplicación funcionará, pero:
- Los requests no se guardarán en Redis
- `/get-responses` devolverá listas vacías
- `/clear-responses` no hará nada

---

## Uso de la API

### Endpoints Públicos (Sin autenticación)

#### 1. **GET /health** - Health Check

Verifica que el servicio esté funcionando.

```bash
curl http://localhost:5000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-16T21:30:00.000000+00:00"
}
```

#### 2. **GET /ping** - Ping

Similar a `/health` pero con respuesta "pong".

```bash
curl http://localhost:5000/ping
```

**Respuesta:**
```json
{
  "status": "pong",
  "timestamp": "2025-10-16T21:30:00.000000+00:00",
  "message": "Service is alive"
}
```

#### 3. **POST /register-token** - Registrar Token

Registra un token JWT para acceder a endpoints protegidos.

```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "mi-token-secreto-123",
    "expiration_seconds": 3600
  }'
```

**Respuesta:**
```json
{
  "message": "Token registered successfully",
  "token": "mi-token-secreto-123",
  "expiration_seconds": 3600
}
```

### Endpoints Protegidos (Requieren autenticación)

Estos endpoints requieren un header `Authorization` con formato `Bearer <token>`.

#### 4. **GET /get-responses** - Obtener Requests Guardados

Obtiene todos los requests guardados en Redis.

**Sin token (ERROR):**
```bash
curl http://localhost:5000/get-responses
```

**Respuesta:**
```json
{
  "error": "Invalid or missing token",
  "message": "Authorization header is required"
}
```

**Con token válido:**
```bash
# Primero registra un token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token-123"}'

# Luego úsalo para acceder al endpoint
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer mi-token-123"
```

**Respuesta:**
```json
{
  "total_returned": 5,
  "redis_connected": true,
  "stats": {
    "connected": true,
    "total_requests": 5,
    "health_requests": 3,
    "ping_requests": 2
  },
  "requests": [
    {
      "endpoint": "/health",
      "ip_address": "127.0.0.1",
      "user_agent": "curl/7.68.0",
      "timestamp": "2025-10-16T21:30:00",
      "additional_data": {"response_status": "ok"}
    }
  ]
}
```

**Con parámetros de filtrado:**
```bash
# Limitar resultados
curl "http://localhost:5000/get-responses?limit=10" \
  -H "Authorization: Bearer mi-token-123"

# Filtrar por endpoint específico
curl "http://localhost:5000/get-responses?endpoint=/health" \
  -H "Authorization: Bearer mi-token-123"

# Combinar filtros
curl "http://localhost:5000/get-responses?endpoint=/health&limit=5" \
  -H "Authorization: Bearer mi-token-123"
```

#### 5. **DELETE /clear-responses** - Eliminar Todos los Requests

Elimina todos los requests guardados en Redis.

```bash
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer mi-token-123"
```

**Respuesta:**
```json
{
  "message": "All responses have been cleared successfully"
}
```

---

## Autenticación con Tokens

### ¿Cómo funciona?

1. **Registrar un token:** Usa el endpoint `/register-token` para guardar un token en Redis
2. **Usar el token:** Incluye el token en el header `Authorization: Bearer <token>`
3. **Expiración:** Los tokens expiran después del tiempo especificado (default: 3600 segundos = 1 hora)

### Ejemplo completo de flujo con autenticación:

```bash
# 1. Registrar un token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "test-token-abc123", "expiration_seconds": 7200}'

# 2. Hacer algunos requests a endpoints públicos (se guardan en Redis)
curl http://localhost:5000/health
curl http://localhost:5000/ping
curl http://localhost:5000/health

# 3. Ver los requests guardados (usando el token)
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token-abc123"

# 4. Limpiar todos los requests (usando el token)
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer test-token-abc123"
```

### Variables de entorno para PowerShell:

```powershell
# Guardar el token en una variable
$TOKEN = "mi-token-secreto-123"

# Registrar el token
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/register-token" `
  -ContentType "application/json" `
  -Body '{"token": "' + $TOKEN + '"}'

# Usar el token en requests
Invoke-RestMethod -Uri "http://localhost:5000/get-responses" `
  -Headers @{Authorization = "Bearer $TOKEN"}
```

---

## Pruebas Automatizadas

El proyecto incluye una suite completa de tests.

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests específicos

```bash
# Tests de endpoints de salud
pytest tests/test_health_endpoint.py -v

# Tests de endpoints Redis
pytest tests/test_redis_endpoints.py -v

# Tests de servicios
pytest tests/test_booking_service.py -v
```

### Ejecutar tests con cobertura

```bash
pytest --cov=src --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador para ver el reporte de cobertura.

---

## Solución de Problemas

### Error: "Redis not available"

**Causa:** Redis no está corriendo o no está accesible.

**Solución:**
```bash
# Verificar si Redis está corriendo
docker ps | grep redis

# Si no está corriendo, iniciarlo
docker run -d -p 6379:6379 --name meet-room-redis redis:7-alpine
```

### Error: "Port 5000 already in use"

**Causa:** Otro proceso está usando el puerto 5000.

**Solución:**
```bash
# En Linux/Mac: Encontrar y matar el proceso
lsof -ti:5000 | xargs kill -9

# En Windows PowerShell:
Get-NetTCPConnection -LocalPort 5000 | Select-Object -ExpandProperty OwningProcess | Stop-Process
```

### Error: "Invalid or missing token"

**Causa:** No has registrado el token o el header Authorization está mal formateado.

**Solución:**
1. Registra un token primero usando `/register-token`
2. Asegúrate de usar el formato: `Authorization: Bearer <token>`
3. Verifica que el token no haya expirado

### Tests fallan con "Connection refused"

**Causa:** Los tests están intentando conectarse a un servidor en ejecución (test_endpoints.py).

**Solución:** Los tests unitarios no necesitan servidor. Usa:
```bash
pytest tests/test_health_endpoint.py tests/test_redis_endpoints.py
```

---

## Modo Consola (Aplicación Original)

El proyecto también incluye un modo consola interactivo para gestión de reservas:

```bash
python -m src.main
```

Este modo no usa Redis y es independiente del servidor web.

---

## Recursos Adicionales

- **README.md**: Documentación general del proyecto
- **TESTING_GUIDE.md**: Guía detallada de pruebas
- **docker-compose.yml**: Configuración de Docker Compose
- **requirements.txt**: Dependencias de Python

---

## Arquitectura del Sistema

```
┌──────────────┐
│   Cliente    │
│ (curl/web)   │
└──────┬───────┘
       │
       │ HTTP
       ▼
┌──────────────────────┐
│   Flask App (5000)   │
│                      │
│  Endpoints:          │
│  - /health           │
│  - /ping             │
│  - /get-responses ⚠️ │
│  - /clear-responses ⚠│
│  - /register-token   │
└──────┬───────────────┘
       │
       │ ⚠️ = Requiere token
       ▼
┌──────────────────────┐
│   Redis (6379)       │
│                      │
│  - Tokens            │
│  - Requests          │
│  - Estadísticas      │
└──────────────────────┘
```

---

## Resumen de Comandos Rápidos

```bash
# Iniciar con Docker Compose (Recomendado)
docker-compose up -d
docker-compose logs -f
docker-compose down

# Iniciar Redis solo
docker run -d -p 6379:6379 --name meet-room-redis redis:7-alpine

# Ejecutar app localmente
python run_web.py

# Registrar token y probar endpoints
curl -X POST http://localhost:5000/register-token -H "Content-Type: application/json" -d '{"token": "test123"}'
curl http://localhost:5000/health
curl http://localhost:5000/get-responses -H "Authorization: Bearer test123"

# Ejecutar tests
pytest -v
```

---

**¡Listo! Ahora puedes ejecutar y usar el proyecto Meeting Room Booking System.** 🎉
