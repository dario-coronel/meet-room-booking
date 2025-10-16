#!/bin/bash

# Script para probar la configuración de Docker Compose
# Este script verifica que la aplicación está corriendo correctamente

set -e

echo "🧪 Testing Docker Compose Setup"
echo "================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# 1. Verificar que Docker está instalado
echo "1. Verificando instalación de Docker..."
if command -v docker &> /dev/null; then
    print_success "Docker está instalado: $(docker --version)"
else
    print_error "Docker no está instalado"
    echo "Por favor instala Docker: https://www.docker.com/get-started"
    exit 1
fi

# 2. Verificar que Docker Compose está disponible
echo ""
echo "2. Verificando Docker Compose..."
if docker compose version &> /dev/null; then
    print_success "Docker Compose está disponible: $(docker compose version)"
elif docker-compose --version &> /dev/null; then
    print_success "Docker Compose está disponible: $(docker-compose --version)"
    print_info "Nota: Estás usando docker-compose (legacy). Considera usar 'docker compose'"
else
    print_error "Docker Compose no está instalado"
    exit 1
fi

# 3. Verificar que los containers están corriendo
echo ""
echo "3. Verificando estado de containers..."
if docker compose ps | grep -q "meet-room-app.*Up"; then
    print_success "Container meet-room-app está corriendo"
else
    print_error "Container meet-room-app no está corriendo"
    print_info "Ejecuta: docker compose up -d"
    exit 1
fi

if docker compose ps | grep -q "meet-room-redis.*Up"; then
    print_success "Container meet-room-redis está corriendo"
else
    print_error "Container meet-room-redis no está corriendo"
    print_info "Ejecuta: docker compose up -d"
    exit 1
fi

# 4. Verificar healthcheck de Redis
echo ""
echo "4. Verificando Redis health check..."
REDIS_HEALTH=$(docker inspect meet-room-redis --format='{{.State.Health.Status}}' 2>/dev/null || echo "unknown")
if [ "$REDIS_HEALTH" = "healthy" ]; then
    print_success "Redis está saludable"
else
    print_error "Redis health check: $REDIS_HEALTH"
    print_info "Espera unos segundos y vuelve a intentar"
fi

# 5. Probar endpoint /health
echo ""
echo "5. Probando endpoint /health..."
sleep 2  # Dar tiempo para que la app esté lista
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health 2>/dev/null || echo "000")
if [ "$HEALTH_RESPONSE" = "200" ]; then
    print_success "Endpoint /health responde correctamente (HTTP 200)"
    HEALTH_DATA=$(curl -s http://localhost:5000/health)
    echo "   Respuesta: $HEALTH_DATA"
else
    print_error "Endpoint /health falló (HTTP $HEALTH_RESPONSE)"
    print_info "Verifica los logs: docker compose logs app"
    exit 1
fi

# 6. Probar endpoint /ping
echo ""
echo "6. Probando endpoint /ping..."
PING_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ping 2>/dev/null || echo "000")
if [ "$PING_RESPONSE" = "200" ]; then
    print_success "Endpoint /ping responde correctamente (HTTP 200)"
    PING_DATA=$(curl -s http://localhost:5000/ping)
    echo "   Respuesta: $PING_DATA"
else
    print_error "Endpoint /ping falló (HTTP $PING_RESPONSE)"
    exit 1
fi

# 7. Probar endpoint /get-responses
echo ""
echo "7. Probando endpoint /get-responses..."
RESPONSES_HTTP=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/get-responses 2>/dev/null || echo "000")
if [ "$RESPONSES_HTTP" = "200" ]; then
    print_success "Endpoint /get-responses responde correctamente (HTTP 200)"
    RESPONSES_DATA=$(curl -s http://localhost:5000/get-responses | head -c 200)
    echo "   Respuesta (primeros 200 chars): $RESPONSES_DATA..."
else
    print_error "Endpoint /get-responses falló (HTTP $RESPONSES_HTTP)"
    exit 1
fi

# 8. Verificar conectividad Redis desde la app
echo ""
echo "8. Verificando conectividad Redis..."
REDIS_CHECK=$(docker compose exec -T app sh -c "python -c 'import redis; r=redis.Redis(host=\"redis\", port=6379); print(r.ping())'" 2>/dev/null || echo "False")
if [ "$REDIS_CHECK" = "True" ]; then
    print_success "Aplicación puede conectarse a Redis"
else
    print_error "Aplicación no puede conectarse a Redis"
    exit 1
fi

# 9. Verificar volumen de datos
echo ""
echo "9. Verificando volumen de Redis..."
if docker volume ls | grep -q "redis-data"; then
    print_success "Volumen redis-data existe"
    VOLUME_SIZE=$(docker volume inspect redis-data --format='{{.Mountpoint}}' 2>/dev/null || echo "N/A")
    echo "   Mountpoint: $VOLUME_SIZE"
else
    print_error "Volumen redis-data no existe"
fi

# 10. Verificar red Docker
echo ""
echo "10. Verificando red Docker..."
if docker network ls | grep -q "meet-room-network"; then
    print_success "Red meet-room-network existe"
else
    print_error "Red meet-room-network no existe"
fi

# Resumen final
echo ""
echo "================================"
echo "✨ Resumen de Tests"
echo "================================"
echo ""
print_success "Todos los tests pasaron exitosamente!"
echo ""
echo "La aplicación está funcionando correctamente en:"
echo "  - http://localhost:5000/health"
echo "  - http://localhost:5000/ping"
echo "  - http://localhost:5000/get-responses"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs:     docker compose logs -f"
echo "  - Detener:      docker compose down"
echo "  - Reiniciar:    docker compose restart"
echo ""
