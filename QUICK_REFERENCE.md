# 🚀 Quick Reference - Meeting Room Booking System

## ⚡ Inicio Rápido (5 minutos)

### 1. Iniciar el proyecto
```bash
docker compose up -d
```

### 2. Verificar que está corriendo
```bash
docker compose ps
```

### 3. Probar endpoints públicos
```bash
curl http://localhost:5000/health
curl http://localhost:5000/ping
```

### 4. Registrar un token
```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token-123"}'
```

### 5. Usar endpoints protegidos
```bash
# Ver requests guardados
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer mi-token-123"

# Limpiar requests
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer mi-token-123"
```

---

## 📋 Endpoints Disponibles

### Públicos (sin autenticación):
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/ping` | Ping/pong check |
| POST | `/register-token` | Registrar token de autenticación |

### Protegidos (requieren token):
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/get-responses` | Obtener requests guardados |
| DELETE | `/clear-responses` | Eliminar todos los requests |

---

## 🔑 Autenticación

Todos los endpoints protegidos requieren un header:
```
Authorization: Bearer <tu-token>
```

**Ejemplo completo:**
```bash
# 1. Registrar token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123", "expiration_seconds": 3600}'

# 2. Usar el token
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer abc123"
```

---

## 🐳 Comandos Docker Compose

```bash
# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f
docker compose logs -f app    # Solo app
docker compose logs -f redis  # Solo Redis

# Ver estado
docker compose ps

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Ver consumo de recursos
docker compose stats
```

---

## 🧪 Comandos de Testing

```bash
# Todos los tests
pytest

# Con información detallada
pytest -v

# Tests específicos
pytest tests/test_health_endpoint.py
pytest tests/test_redis_endpoints.py

# Con cobertura
pytest --cov=src --cov-report=html
```

---

## 📊 Ejemplos de Uso Real

### Ejemplo 1: Monitorear salud del sistema
```bash
# Hacer varios requests
curl http://localhost:5000/health
curl http://localhost:5000/ping
curl http://localhost:5000/health

# Ver estadísticas
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer mi-token"
```

### Ejemplo 2: Filtrar requests
```bash
# Solo requests de /health
curl "http://localhost:5000/get-responses?endpoint=/health" \
  -H "Authorization: Bearer mi-token"

# Últimos 5 requests
curl "http://localhost:5000/get-responses?limit=5" \
  -H "Authorization: Bearer mi-token"

# Combinado
curl "http://localhost:5000/get-responses?endpoint=/health&limit=10" \
  -H "Authorization: Bearer mi-token"
```

### Ejemplo 3: Limpiar datos
```bash
# Eliminar todos los requests guardados
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer mi-token"
```

---

## 🔍 Verificar Redis directamente

```bash
# Conectarse a Redis
docker compose exec redis redis-cli

# Comandos útiles dentro de redis-cli:
KEYS *                    # Ver todas las claves
LLEN all_requests         # Contar requests
ZCARD requests:/health    # Contar requests de /health
GET token:mi-token        # Ver si un token existe
TTL token:mi-token        # Ver tiempo restante del token
DEL all_requests          # Limpiar requests manualmente
```

---

## 🔧 Solución de Problemas

### Puerto 5000 ocupado
```bash
# Cambiar puerto en docker-compose.yml:
ports:
  - "5001:5000"  # Usar 5001 en lugar de 5000
```

### Redis no conecta
```bash
# Verificar que Redis esté corriendo
docker compose ps

# Ver logs de Redis
docker compose logs redis

# Reiniciar Redis
docker compose restart redis
```

### Token no funciona
```bash
# Verificar que el token esté en Redis
docker compose exec redis redis-cli EXISTS token:mi-token

# Si retorna 0, el token no existe o expiró
# Registrar nuevamente
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token"}'
```

---

## 📚 Documentación Completa

- **[EJECUCION.md](./EJECUCION.md)** - Guía completa de ejecución paso a paso
- **[RESUMEN_FUNCIONALIDADES.md](./RESUMEN_FUNCIONALIDADES.md)** - Detalles de todas las funcionalidades
- **[README.md](./README.md)** - Documentación general del proyecto
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - Guía de testing

---

## 🎯 Casos de Uso Comunes

### Desarrollo local
```bash
# 1. Iniciar Redis solo
docker run -d -p 6379:6379 --name redis redis:7-alpine

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar app localmente
python run_web.py
```

### Producción
```bash
# Usar Docker Compose
docker compose up -d

# Monitorear logs
docker compose logs -f
```

### Testing
```bash
# Ejecutar tests
pytest -v

# Con cobertura
pytest --cov=src --cov-report=term
```

---

## 💡 Tips

1. **Token de desarrollo**: Usa tokens simples para desarrollo local
   ```bash
   {"token": "dev-token", "expiration_seconds": 86400}  # 24 horas
   ```

2. **Ver JSON formateado**: Usa `jq` o Python para formatear
   ```bash
   curl http://localhost:5000/health | python -m json.tool
   curl http://localhost:5000/health | jq .
   ```

3. **Variables de entorno**: PowerShell
   ```powershell
   $TOKEN = "mi-token"
   $HEADERS = @{Authorization = "Bearer $TOKEN"}
   Invoke-RestMethod -Uri "http://localhost:5000/get-responses" -Headers $HEADERS
   ```

4. **Backup de Redis**: Los datos persisten en un volumen Docker
   ```bash
   docker compose exec redis redis-cli SAVE
   ```

---

## 🆘 Ayuda Rápida

```bash
# Estado de servicios
docker compose ps

# Logs en tiempo real
docker compose logs -f

# Reiniciar todo
docker compose restart

# Limpiar y empezar de cero
docker compose down -v
docker compose up -d

# Ejecutar tests
pytest -v

# Ver ayuda de comandos
docker compose --help
pytest --help
```

---

**Última actualización:** 2025-10-16  
**Version:** 1.0  
**Tests:** 32/32 ✅
