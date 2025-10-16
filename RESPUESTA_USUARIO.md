# 🎉 Respuesta: Cómo Ejecutar el Proyecto

## ✅ Buenas Noticias: ¡Todo Está Listo!

El proyecto **ya tiene todas las funcionalidades implementadas** que solicitaste:

1. ✅ Redis con Docker para almacenar datos de health requests
2. ✅ Endpoint `GET /get-responses` para obtener todos los requests guardados
3. ✅ Endpoint `DELETE /clear-responses` para eliminar todos los requests
4. ✅ Middleware de validación de tokens en el header
5. ✅ 32 tests automatizados (todos pasando)

---

## 🚀 Cómo Ejecutar el Proyecto (Forma Más Fácil)

### Opción 1: Docker Compose (Recomendado - Todo en Uno)

Esta es la forma **más simple** y **completa** de ejecutar el proyecto:

```bash
# 1. Clonar el repositorio (si aún no lo hiciste)
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking

# 2. Iniciar TODOS los servicios (Redis + App)
docker compose up -d

# 3. Verificar que están corriendo
docker compose ps

# 4. Ver los logs
docker compose logs -f app
```

**¡Eso es todo!** La aplicación estará disponible en `http://localhost:5000`

---

## 📱 Probar los Endpoints

### Paso 1: Probar endpoints públicos (no requieren autenticación)

```bash
# Health check
curl http://localhost:5000/health

# Ping
curl http://localhost:5000/ping
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-16T21:30:00.000000+00:00"
}
```

### Paso 2: Registrar un token para endpoints protegidos

```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token-123", "expiration_seconds": 3600}'
```

**Respuesta esperada:**
```json
{
  "message": "Token registered successfully",
  "token": "mi-token-123",
  "expiration_seconds": 3600
}
```

### Paso 3: Usar endpoints protegidos (requieren token)

```bash
# Ver todos los requests guardados
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer mi-token-123"

# Filtrar por endpoint
curl "http://localhost:5000/get-responses?endpoint=/health&limit=10" \
  -H "Authorization: Bearer mi-token-123"

# Eliminar todos los requests
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer mi-token-123"
```

---

## 📊 Tabla Resumen de Endpoints

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| GET | `/health` | ❌ No | Health check del sistema |
| GET | `/ping` | ❌ No | Verificar que el servicio está vivo |
| POST | `/register-token` | ❌ No | Registrar un token para autenticación |
| GET | `/get-responses` | ✅ Sí | Obtener todos los requests guardados |
| DELETE | `/clear-responses` | ✅ Sí | Eliminar todos los requests guardados |

---

## 🔑 Sobre la Autenticación

Los endpoints **protegidos** (`/get-responses` y `/clear-responses`) requieren:

1. **Registrar un token** primero usando `/register-token`
2. **Incluir el token** en cada request usando el header:
   ```
   Authorization: Bearer <tu-token>
   ```

### Ejemplo completo de flujo:

```bash
# 1. Registrar token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123"}'

# 2. Hacer algunos requests (se guardan automáticamente en Redis)
curl http://localhost:5000/health
curl http://localhost:5000/ping
curl http://localhost:5000/health

# 3. Ver los requests guardados (usando el token)
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer abc123"

# Respuesta:
# {
#   "total_returned": 3,
#   "redis_connected": true,
#   "stats": {
#     "total_requests": 3,
#     "health_requests": 2,
#     "ping_requests": 1
#   },
#   "requests": [...]
# }

# 4. Limpiar todo (usando el token)
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer abc123"
```

---

## 🐳 Comandos Docker Compose Útiles

```bash
# Iniciar servicios
docker compose up -d

# Ver estado
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Ver logs solo de la app
docker compose logs -f app

# Ver logs solo de Redis
docker compose logs -f redis

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Ver consumo de recursos
docker compose stats
```

---

## 📚 Documentación Completa Disponible

He creado **4 documentos completos** para ayudarte:

1. **[EJECUCION.md](./EJECUCION.md)** (12KB)
   - Guía paso a paso súper detallada
   - 3 opciones de ejecución diferentes
   - Ejemplos de todos los endpoints
   - Solución de problemas comunes

2. **[RESUMEN_FUNCIONALIDADES.md](./RESUMEN_FUNCIONALIDADES.md)** (13KB)
   - Confirmación de todas las funcionalidades implementadas
   - Arquitectura del sistema
   - Detalles técnicos de cada endpoint
   - Estructura de Redis

3. **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** (6KB)
   - Referencia rápida de comandos
   - Ejemplos de uso común
   - Tips y trucos
   - Solución de problemas

4. **[README.md](./README.md)** (actualizado)
   - Quick start
   - Descripción general del proyecto
   - Links a toda la documentación

---

## 🧪 Tests

El proyecto tiene **32 tests automatizados** (todos pasando):

```bash
# Ejecutar todos los tests
pytest

# Tests con información detallada
pytest -v

# Tests de endpoints específicos
pytest tests/test_redis_endpoints.py -v
pytest tests/test_health_endpoint.py -v
```

**Resultado:**
```
============================== 32 passed in 2.30s ==============================
```

---

## 💡 Resumen de lo que Tienes

### Funcionalidades Implementadas:

✅ **Redis con Docker**
- Configurado en `docker-compose.yml`
- Persistencia de datos habilitada
- Health check configurado

✅ **GET /get-responses**
- Obtiene todos los requests guardados
- Filtros: `?limit=10` y `?endpoint=/health`
- Requiere autenticación Bearer token

✅ **DELETE /clear-responses**
- Elimina todos los requests de Redis
- Requiere autenticación Bearer token
- Respuesta de confirmación

✅ **Middleware de Validación de Token**
- Valida formato `Bearer <token>`
- Verifica token en Redis
- Respuestas de error claras (401)

✅ **Sistema Completo de Autenticación**
- Registro de tokens con expiración
- Validación en cada request
- Tokens almacenados en Redis

---

## 🎯 Siguiente Paso: Probar Todo

```bash
# 1. Iniciar el proyecto
docker compose up -d

# 2. Abrir otra terminal y ejecutar estos comandos:

# Registrar token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "test-token"}'

# Hacer requests
curl http://localhost:5000/health
curl http://localhost:5000/ping

# Ver requests guardados
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token"
```

---

## ❓ ¿Tienes Problemas?

### Redis no conecta:
```bash
docker compose logs redis
docker compose restart redis
```

### Puerto 5000 ocupado:
Edita `docker-compose.yml` y cambia el puerto:
```yaml
ports:
  - "5001:5000"  # Usar puerto 5001
```

### Token no funciona:
```bash
# Verificar en Redis
docker compose exec redis redis-cli GET token:mi-token

# Si no existe, registrar de nuevo
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "mi-token"}'
```

---

## 📞 Documentos de Referencia

- **Inicio rápido**: [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Guía completa**: [EJECUCION.md](./EJECUCION.md)
- **Funcionalidades**: [RESUMEN_FUNCIONALIDADES.md](./RESUMEN_FUNCIONALIDADES.md)
- **Testing**: [TESTING_GUIDE.md](./TESTING_GUIDE.md)

---

## 🎉 ¡Listo!

**Tu proyecto está completamente funcional y documentado.**

Para comenzar, simplemente ejecuta:
```bash
docker compose up -d
```

Y sigue los ejemplos de arriba para probar todos los endpoints.

**¡Éxito con tu proyecto!** 🚀

---

**Fecha:** 2025-10-16  
**Estado:** ✅ Producción Ready  
**Tests:** 32/32 pasando  
**Documentación:** Completa en español
