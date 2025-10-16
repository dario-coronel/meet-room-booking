# 🐳 Guía de Docker Compose - Meeting Room Booking

Esta guía explica cómo ejecutar el proyecto usando Docker Compose de manera simple y rápida.

## 📋 Pre-requisitos

Antes de comenzar, asegúrate de tener instalado:

- **Docker Desktop** (Windows/Mac) o **Docker Engine** (Linux)
- **Docker Compose** (incluido en Docker Desktop)

### Verificar instalación

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker compose version
```

Si ves las versiones instaladas, ¡estás listo para continuar!

---

## 🚀 Cómo ejecutar el proyecto con Docker Compose

### Paso 1: Clonar el repositorio (si aún no lo has hecho)

```bash
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking
```

### Paso 2: Iniciar todos los servicios

```bash
docker compose up -d
```

**¿Qué hace este comando?**
- `docker compose up`: Inicia los servicios definidos en `docker-compose.yml`
- `-d`: Ejecuta los contenedores en segundo plano (modo "detached")

**Servicios que se inician:**
- 🗄️ **Redis**: Base de datos en memoria (puerto 6379)
- 🚀 **App**: Aplicación Flask (puerto 5000)

La primera vez que ejecutes este comando, Docker descargará las imágenes necesarias y construirá la aplicación. Esto puede tardar unos minutos.

### Paso 3: Verificar que los servicios están corriendo

```bash
docker compose ps
```

Deberías ver algo similar a:

```
NAME               IMAGE                    STATUS         PORTS
meet-room-app      meet-room-booking-app    Up             0.0.0.0:5000->5000/tcp
meet-room-redis    redis:7-alpine           Up (healthy)   0.0.0.0:6379->6379/tcp
```

### Paso 4: Probar la aplicación

Abre tu navegador web o usa `curl` para probar los endpoints:

#### Opción A: Navegador Web
- Health check: http://localhost:5000/health
- Ping: http://localhost:5000/ping
- Ver historial de requests: http://localhost:5000/get-responses

#### Opción B: Línea de comandos (curl)

```bash
# Health check
curl http://localhost:5000/health

# Ping
curl http://localhost:5000/ping

# Ver todas las peticiones almacenadas
curl http://localhost:5000/get-responses

# Ver últimas 10 peticiones
curl http://localhost:5000/get-responses?limit=10

# Ver solo peticiones al endpoint /health
curl http://localhost:5000/get-responses?endpoint=/health
```

---

## 📊 Comandos útiles de Docker Compose

### Ver logs en tiempo real

```bash
# Logs de todos los servicios
docker compose logs -f

# Logs solo de la aplicación
docker compose logs -f app

# Logs solo de Redis
docker compose logs -f redis
```

### Detener los servicios

```bash
# Detener sin eliminar los contenedores
docker compose stop

# Detener y eliminar los contenedores
docker compose down

# Detener y eliminar contenedores + volúmenes (borra datos de Redis)
docker compose down -v
```

### Reiniciar los servicios

```bash
# Reiniciar todos los servicios
docker compose restart

# Reiniciar solo un servicio
docker compose restart app
```

### Reconstruir la aplicación después de cambios en el código

```bash
# Reconstruir y reiniciar
docker compose up -d --build

# O en pasos separados:
docker compose build
docker compose up -d
```

### Ver el estado de los servicios

```bash
docker compose ps
```

### Ejecutar comandos dentro de un contenedor

```bash
# Abrir una shell en el contenedor de la app
docker compose exec app /bin/bash

# Ejecutar Python en modo consola (aplicación original)
docker compose exec app python -m src.main

# Conectarse a Redis CLI
docker compose exec redis redis-cli
```

---

## 🔧 Solución de problemas comunes

### Error: "port is already allocated"

**Problema:** El puerto 5000 o 6379 ya está en uso.

**Solución:**
```bash
# Ver qué está usando el puerto 5000
# Windows PowerShell:
netstat -ano | findstr :5000

# Linux/Mac:
lsof -i :5000

# Detener el proceso o cambiar el puerto en docker-compose.yml
```

### Error: "Cannot connect to Redis"

**Problema:** Redis no está disponible.

**Solución:**
```bash
# Verificar que Redis está healthy
docker compose ps

# Ver logs de Redis
docker compose logs redis

# Reiniciar Redis
docker compose restart redis
```

### La aplicación no refleja cambios en el código

**Problema:** Necesitas reconstruir la imagen.

**Solución:**
```bash
# Reconstruir la imagen de la app
docker compose up -d --build
```

### Limpiar todo y empezar de cero

```bash
# Detener y eliminar todo (contenedores, redes, volúmenes)
docker compose down -v

# Eliminar imágenes construidas
docker rmi meet-room-booking-app

# Volver a iniciar
docker compose up -d --build
```

---

## 📝 Detalles técnicos

### Estructura de docker-compose.yml

El archivo `docker-compose.yml` define dos servicios:

1. **redis**: 
   - Imagen: `redis:7-alpine`
   - Puerto: 6379
   - Persistencia: Volumen `redis-data`
   - Health check automático

2. **app**:
   - Build: Construye desde `Dockerfile`
   - Puerto: 5000
   - Variables de entorno:
     - `REDIS_HOST=redis`
     - `REDIS_PORT=6379`
     - `REDIS_DB=0`
   - Depende de: Redis (espera a que esté healthy)

### Redes

Los servicios se comunican a través de la red interna `meet-room-network`:
- La app puede conectarse a Redis usando el hostname `redis`
- Redis no es accesible directamente desde fuera (solo a través de la app)

### Volúmenes

- `redis-data`: Persiste los datos de Redis entre reinicios

---

## 🎯 Accesos rápidos

| Servicio | URL | Descripción |
|----------|-----|-------------|
| App - Health Check | http://localhost:5000/health | Estado de la aplicación |
| App - Ping | http://localhost:5000/ping | Verificar que el servicio responde |
| App - Get Responses | http://localhost:5000/get-responses | Ver historial de peticiones |
| Redis | localhost:6379 | Redis DB (solo accesible localmente) |

---

## 🆘 ¿Necesitas más ayuda?

- Ver documentación completa: [README.md](README.md)
- Reportar problemas: [GitHub Issues](https://github.com/dario-coronel/meet-room-booking/issues)

---

**¡Listo!** 🎉 Ya sabes cómo ejecutar el proyecto con Docker Compose.
