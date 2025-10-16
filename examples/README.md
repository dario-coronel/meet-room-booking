# 📚 Ejemplos y Scripts de Utilidad

Esta carpeta contiene scripts y ejemplos para facilitar el uso del proyecto.

## Scripts Disponibles

### test-docker-setup.sh

Script de verificación para probar que Docker Compose está configurado correctamente.

**Uso:**
```bash
# Primero, inicia los servicios
docker compose up -d

# Luego, ejecuta el script de validación
./examples/test-docker-setup.sh
```

**¿Qué verifica?**
- ✅ Docker y Docker Compose están instalados
- ✅ Containers están corriendo
- ✅ Redis está saludable
- ✅ Endpoints HTTP responden correctamente
- ✅ Conectividad entre app y Redis
- ✅ Volúmenes y redes están configurados

**Output esperado:**
```
🧪 Testing Docker Compose Setup
================================

1. Verificando instalación de Docker...
✓ Docker está instalado: Docker version 24.0.0
...
✓ Todos los tests pasaron exitosamente!
```

## Casos de Uso

### Verificar setup después de clonar el repositorio

```bash
# 1. Clonar y entrar al repositorio
git clone https://github.com/dario-coronel/meet-room-booking.git
cd meet-room-booking

# 2. Iniciar servicios
docker compose up -d

# 3. Verificar que todo funciona
./examples/test-docker-setup.sh
```

### Debugging cuando algo no funciona

```bash
# Ejecutar el script para identificar el problema
./examples/test-docker-setup.sh

# El script te dirá exactamente qué está fallando:
# - Si Docker no está instalado
# - Si los containers no están corriendo
# - Si Redis no responde
# - Si los endpoints HTTP fallan
# etc.
```

### Validar cambios antes de commit

```bash
# Después de hacer cambios al código
docker compose up -d --build

# Validar que todo sigue funcionando
./examples/test-docker-setup.sh
```

## Próximos Scripts (Coming Soon)

- `load-test.sh`: Script para probar carga en los endpoints
- `backup-redis.sh`: Script para hacer backup de datos de Redis
- `deploy-production.sh`: Script para desplegar en producción
- `dev-setup.sh`: Script para configurar entorno de desarrollo

## Contribuir

Si tienes ideas para scripts útiles, ¡crea un PR!
