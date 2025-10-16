# Guía de prueba del sistema con Redis

## Opción 1: Con Docker Desktop (Recomendado)

### Prerequisito:
1. Iniciar Docker Desktop
2. Esperar a que el ícono de Docker esté verde

### Comandos:
```powershell
# Levantar servicios (Redis + App)
docker compose up -d

# Verificar que estén corriendo
docker compose ps

# Ver logs
docker compose logs -f app

# Probar endpoints públicos (sin autenticación)
curl http://localhost:5000/health
curl http://localhost:5000/ping

# Registrar un token para endpoints protegidos
curl -X POST http://localhost:5000/register-token -H "Content-Type: application/json" -d '{"token": "test-token-123"}'

# Probar endpoints protegidos (con autenticación)
curl http://localhost:5000/get-responses -H "Authorization: Bearer test-token-123"
curl -X DELETE http://localhost:5000/clear-responses -H "Authorization: Bearer test-token-123"
```

---

## Opción 2: Redis en Docker, App local (Alternativa)

### Paso 1: Levantar solo Redis
```powershell
docker run -d -p 6379:6379 --name meet-room-redis redis:7-alpine
```

### Paso 2: Ejecutar app localmente
```powershell
# Activar venv
& .\.venv\Scripts\Activate.ps1

# Ejecutar servidor
python run_web.py
```

### Paso 3: Probar endpoints
```powershell
# Desde otra terminal PowerShell

# Endpoints públicos
curl http://localhost:5000/health
curl http://localhost:5000/ping

# Registrar token
curl -X POST http://localhost:5000/register-token -H "Content-Type: application/json" -d '{"token": "test-123"}'

# Endpoints protegidos (con token)
curl http://localhost:5000/get-responses -H "Authorization: Bearer test-123"
```

---

## Opción 3: Sin Docker (Solo testing)

Si no tienes Docker, la app funcionará pero sin persistencia Redis:
- Los endpoints responderán normalmente
- Redis no guardará los requests
- `/get-responses` devolverá lista vacía

```powershell
python run_web.py
# Acceder a http://localhost:5000/health
```

---

## Tests automatizados (sin necesidad de Redis)

Los tests funcionan con mocks:
```powershell
pytest tests/test_redis_endpoints.py -v
pytest tests/test_health_endpoint.py -v
```

---

## Verificación de endpoints

### /health
```bash
curl http://localhost:5000/health
# Respuesta esperada:
# {"status":"ok","timestamp":"2025-10-07T..."}
```

### /ping
```bash
curl http://localhost:5000/ping
# Respuesta esperada:
# {"status":"pong","timestamp":"2025-10-07T...","message":"Service is alive"}
```

### /get-responses
```bash
# Primero registrar un token
curl -X POST http://localhost:5000/register-token -H "Content-Type: application/json" -d '{"token": "my-token"}'

# Todos los requests (requiere autenticación)
curl http://localhost:5000/get-responses -H "Authorization: Bearer my-token"

# Con límite
curl "http://localhost:5000/get-responses?limit=5" -H "Authorization: Bearer my-token"

# Filtrar por endpoint
curl "http://localhost:5000/get-responses?endpoint=/health" -H "Authorization: Bearer my-token"
```
