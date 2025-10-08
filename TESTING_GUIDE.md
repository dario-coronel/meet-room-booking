# Guía de prueba del sistema con Redis

## Opción 1: Con Docker Desktop (Recomendado)

### Prerequisito:
1. Iniciar Docker Desktop
2. Esperar a que el ícono de Docker esté verde

### Comandos:
```powershell
# Levantar servicios (Redis + App)
docker-compose up -d

# Verificar que estén corriendo
docker-compose ps

# Ver logs
docker-compose logs -f app

# Probar endpoints
curl http://localhost:5000/health
curl http://localhost:5000/ping
curl http://localhost:5000/get-responses
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
curl http://localhost:5000/health
curl http://localhost:5000/ping
curl http://localhost:5000/get-responses
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
# Todos los requests
curl http://localhost:5000/get-responses

# Con límite
curl "http://localhost:5000/get-responses?limit=5"

# Filtrar por endpoint
curl "http://localhost:5000/get-responses?endpoint=/health"
```
