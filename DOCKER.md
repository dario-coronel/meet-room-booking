# 🐳 Guía Completa de Docker y Docker Compose

Esta guía detalla cómo ejecutar el proyecto Meeting Room Booking System usando Docker y Docker Compose.

## Tabla de Contenidos
- [Prerrequisitos](#prerrequisitos)
- [Opción 1: Docker Compose (Recomendado)](#opción-1-docker-compose-recomendado)
- [Opción 2: Docker Manual](#opción-2-docker-manual)
- [Variables de Entorno](#variables-de-entorno)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Prerrequisitos

### Instalar Docker

**Windows / Mac:**
1. Descargar [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Ejecutar el instalador
3. Docker Compose viene incluido

**Linux (Ubuntu/Debian):**
```bash
# Actualizar paquetes
sudo apt-get update

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get install docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión para aplicar cambios
```

**Verificar instalación:**
```bash
docker --version
docker compose version
```

## Opción 1: Docker Compose (Recomendado)

Docker Compose es la forma más sencilla de ejecutar el proyecto porque:
- ✅ Levanta Redis y la aplicación automáticamente
- ✅ Configura la red entre containers
- ✅ Gestiona volúmenes para persistencia
- ✅ Un solo comando para iniciar/detener todo

### Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking

# Iniciar servicios
docker compose up -d

# Verificar que funciona
curl http://localhost:5000/health
```

### Comandos Comunes

#### Iniciar servicios
```bash
# Modo detached (en background)
docker compose up -d

# Modo foreground (ver logs en tiempo real)
docker compose up

# Reconstruir imágenes antes de iniciar
docker compose up --build -d
```

#### Ver logs
```bash
# Todos los servicios
docker compose logs -f

# Solo aplicación
docker compose logs -f app

# Solo Redis
docker compose logs -f redis

# Ver últimas 100 líneas
docker compose logs --tail=100 app
```

#### Gestionar servicios
```bash
# Ver estado de containers
docker compose ps

# Detener servicios (mantiene datos)
docker compose down

# Detener y eliminar volúmenes (borra datos)
docker compose down -v

# Reiniciar servicios
docker compose restart

# Reiniciar solo la app
docker compose restart app
```

#### Ejecutar comandos dentro de containers
```bash
# Acceder a shell de la aplicación
docker compose exec app bash

# Ejecutar modo consola interactivo
docker compose exec app python -m src.main

# Ejecutar tests
docker compose exec app pytest

# Ver variables de entorno
docker compose exec app env
```

#### Scaling (múltiples instancias)
```bash
# Iniciar 3 instancias de la app
docker compose up -d --scale app=3

# Nota: Necesitarás un load balancer para distribuir tráfico
```

### Estructura del docker-compose.yml

```yaml
services:
  redis:
    image: redis:7-alpine        # Imagen oficial de Redis
    container_name: meet-room-redis
    ports:
      - "6379:6379"              # Puerto expuesto
    volumes:
      - redis-data:/data          # Persistencia de datos
    command: redis-server --appendonly yes  # AOF para durabilidad
    healthcheck:                  # Verificación de salud
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - meet-room-network         # Red privada

  app:
    build: .                      # Construir desde Dockerfile local
    container_name: meet-room-app
    ports:
      - "5000:5000"               # Puerto Flask
    environment:
      - REDIS_HOST=redis          # Hostname de Redis en la red Docker
      - REDIS_PORT=6379
      - REDIS_DB=0
    depends_on:
      redis:
        condition: service_healthy  # Espera a que Redis esté listo
    networks:
      - meet-room-network

volumes:
  redis-data:                     # Volumen para persistencia

networks:
  meet-room-network:              # Red privada para los servicios
    driver: bridge
```

## Opción 2: Docker Manual

Si prefieres tener más control, puedes ejecutar los containers manualmente.

### 1. Crear una red Docker

```bash
docker network create meet-room-network
```

### 2. Iniciar Redis

```bash
docker run -d \
  --name meet-room-redis \
  --network meet-room-network \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:7-alpine redis-server --appendonly yes
```

### 3. Construir imagen de la aplicación

```bash
docker build -t meet-room-booking .
```

### 4. Ejecutar aplicación

```bash
docker run -d \
  --name meet-room-app \
  --network meet-room-network \
  -p 5000:5000 \
  -e REDIS_HOST=meet-room-redis \
  -e REDIS_PORT=6379 \
  -e REDIS_DB=0 \
  meet-room-booking
```

### 5. Verificar

```bash
# Ver logs
docker logs -f meet-room-app

# Probar endpoint
curl http://localhost:5000/health
```

### 6. Limpiar

```bash
# Detener containers
docker stop meet-room-app meet-room-redis

# Eliminar containers
docker rm meet-room-app meet-room-redis

# Eliminar red
docker network rm meet-room-network

# Eliminar volumen (opcional)
docker volume rm redis-data
```

## Variables de Entorno

La aplicación soporta las siguientes variables de entorno:

| Variable | Descripción | Valor por defecto | Requerida |
|----------|-------------|-------------------|-----------|
| `REDIS_HOST` | Hostname del servidor Redis | `localhost` | Sí |
| `REDIS_PORT` | Puerto de Redis | `6379` | No |
| `REDIS_DB` | Número de base de datos Redis | `0` | No |
| `FLASK_ENV` | Entorno de Flask (`development`/`production`) | `production` | No |
| `FLASK_DEBUG` | Modo debug de Flask | `False` | No |

### Ejemplo con variables personalizadas

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=1          # Usar DB 1 en lugar de 0
      - FLASK_ENV=development
      - FLASK_DEBUG=True
```

**Docker manual:**
```bash
docker run -d \
  -e REDIS_HOST=meet-room-redis \
  -e REDIS_PORT=6379 \
  -e REDIS_DB=1 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=True \
  -p 5000:5000 \
  meet-room-booking
```

## Troubleshooting

### Problema: "Cannot connect to the Docker daemon"

**Causa:** Docker no está corriendo.

**Solución:**
```bash
# Windows/Mac: Abrir Docker Desktop

# Linux:
sudo systemctl start docker
sudo systemctl enable docker
```

### Problema: "Port 5000 is already in use"

**Causa:** Otro proceso está usando el puerto 5000.

**Solución 1 - Cambiar puerto en docker-compose.yml:**
```yaml
services:
  app:
    ports:
      - "8080:5000"  # Usar puerto 8080 en lugar de 5000
```

**Solución 2 - Detener proceso en puerto 5000:**
```bash
# Linux/Mac
sudo lsof -i :5000
sudo kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problema: "Error connecting to Redis"

**Verificar que Redis está corriendo:**
```bash
docker compose ps redis

# Debería mostrar:
# NAME              IMAGE           STATUS
# meet-room-redis   redis:7-alpine  Up (healthy)
```

**Verificar conectividad:**
```bash
# Probar conexión desde la app
docker compose exec app bash -c "nc -zv redis 6379"

# Debería mostrar:
# redis (172.x.x.x:6379) open
```

**Ver logs de Redis:**
```bash
docker compose logs redis

# Buscar errores o advertencias
```

**Solución:**
```bash
# Reiniciar Redis
docker compose restart redis

# O reconstruir todo
docker compose down -v
docker compose up -d
```

### Problema: "Image build failed"

**Causa:** Error al construir la imagen Docker (usualmente por dependencias).

**Solución:**
```bash
# Reconstruir sin caché
docker compose build --no-cache

# Ver logs detallados
docker compose build --progress=plain
```

### Problema: Cambios en código no se reflejan

**Causa:** La imagen no se reconstruyó con los cambios.

**Solución:**
```bash
# Reconstruir imagen
docker compose build app

# O reconstruir y reiniciar
docker compose up -d --build
```

### Problema: "Volume is in use"

**Causa:** Intentar eliminar volumen mientras está en uso.

**Solución:**
```bash
# Detener containers primero
docker compose down

# Luego eliminar volúmenes
docker compose down -v
```

### Problema: Container crashea inmediatamente

**Ver logs para diagnosticar:**
```bash
docker compose logs app

# Ver últimas líneas
docker compose logs --tail=50 app
```

**Causas comunes:**
- Error en el código Python
- Dependencias faltantes
- Puerto ya en uso
- Redis no disponible

## FAQ

### ¿Cómo accedo al modo consola con Docker Compose?

```bash
docker compose exec app python -m src.main
```

### ¿Cómo ejecuto los tests?

```bash
# Con Docker Compose
docker compose exec app pytest

# Con coverage
docker compose exec app pytest --cov=src

# Tests específicos
docker compose exec app pytest tests/test_health_endpoint.py -v
```

### ¿Cómo persisto los datos de Redis?

Los datos se guardan automáticamente en el volumen `redis-data`. Para respaldo:

```bash
# Crear backup
docker compose exec redis redis-cli BGSAVE
docker compose exec redis redis-cli LASTSAVE

# Copiar datos del volumen
docker run --rm -v redis-data:/data -v $(pwd):/backup ubuntu tar czf /backup/redis-backup.tar.gz /data
```

### ¿Cómo actualizo la aplicación?

```bash
# 1. Pull últimos cambios
git pull origin main

# 2. Reconstruir y reiniciar
docker compose up -d --build

# 3. Verificar
curl http://localhost:5000/health
```

### ¿Cómo limpio todo (containers, imágenes, volúmenes)?

```bash
# Detener y eliminar todo
docker compose down -v --rmi all

# Eliminar imágenes huérfanas
docker image prune -a

# Eliminar volúmenes no usados
docker volume prune
```

### ¿Puedo usar Docker Compose para producción?

Sí, pero considera:
- Usar `restart: always` para auto-reinicio
- Configurar límites de recursos
- Usar secretos para credenciales
- Implementar monitoreo y logging
- Usar nginx como reverse proxy

**Ejemplo para producción:**
```yaml
services:
  app:
    build: .
    restart: always
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### ¿Cómo configuro HTTPS?

Necesitas un reverse proxy como nginx o traefik. Ejemplo con nginx:

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - app
```

## Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Redis Docker Image](https://hub.docker.com/_/redis)

## Soporte

Si encuentras problemas no cubiertos en esta guía:
1. Revisa los [issues del repositorio](https://github.com/dario-coronel/meet-room-booking/issues)
2. Crea un nuevo issue con:
   - Comando ejecutado
   - Mensaje de error completo
   - Output de `docker compose ps` y `docker compose logs`
   - Versión de Docker (`docker --version`)
