# API Usage Guide - Meeting Room Booking System

This guide demonstrates how to use all the Redis-integrated endpoints with token authentication.

## Quick Start

### 1. Start Redis (with Docker)
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

### 2. Start the Flask Application
```bash
# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6379

# Run the application
python run_web.py
```

The application will be available at `http://localhost:5000`

## Available Endpoints

### Public Endpoints (No Authentication Required)

#### GET /health
Health check endpoint that persists request data to Redis.

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-16T21:52:05.541103+00:00"
}
```

#### GET /ping
Ping endpoint to verify service availability.

```bash
curl http://localhost:5000/ping
```

**Response:**
```json
{
  "status": "pong",
  "timestamp": "2025-10-16T21:52:11.579685+00:00",
  "message": "Service is alive"
}
```

#### POST /register-token
Register a JWT token for authentication (for testing purposes).

```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "my-test-token-123",
    "expiration_seconds": 3600
  }'
```

**Response:**
```json
{
  "message": "Token registered successfully",
  "token": "my-test-token-123",
  "expiration_seconds": 3600
}
```

**Note:** For production use, generate a proper JWT token from https://www.jwt.io/

---

### Protected Endpoints (Authentication Required)

All protected endpoints require an `Authorization` header with a Bearer token:
```
Authorization: Bearer <your-token>
```

#### GET /get-responses
Retrieve all persisted requests from Redis.

**Without authentication (will fail):**
```bash
curl http://localhost:5000/get-responses
```

**Response:**
```json
{
  "error": "Invalid or missing token",
  "message": "Authorization header is required"
}
```

**With valid token:**
```bash
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer my-test-token-123"
```

**Response:**
```json
{
  "total_returned": 2,
  "redis_connected": true,
  "stats": {
    "connected": true,
    "total_requests": 2,
    "health_requests": 1,
    "ping_requests": 1
  },
  "requests": [
    {
      "endpoint": "/ping",
      "ip_address": "127.0.0.1",
      "user_agent": "curl/8.5.0",
      "timestamp": "2025-10-16T21:52:11.580120",
      "additional_data": {
        "response": "pong"
      }
    },
    {
      "endpoint": "/health",
      "ip_address": "127.0.0.1",
      "user_agent": "curl/8.5.0",
      "timestamp": "2025-10-16T21:52:05.541551",
      "additional_data": {
        "response_status": "ok"
      }
    }
  ]
}
```

**Query Parameters:**

- `limit` (default: 100): Maximum number of requests to return
  ```bash
  curl "http://localhost:5000/get-responses?limit=10" \
    -H "Authorization: Bearer my-test-token-123"
  ```

- `endpoint`: Filter by specific endpoint (e.g., `/health` or `/ping`)
  ```bash
  curl "http://localhost:5000/get-responses?endpoint=/health" \
    -H "Authorization: Bearer my-test-token-123"
  ```

#### DELETE /clear-responses
Delete all persisted responses from Redis.

**Without authentication (will fail):**
```bash
curl -X DELETE http://localhost:5000/clear-responses
```

**With valid token:**
```bash
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer my-test-token-123"
```

**Response:**
```json
{
  "message": "All responses have been cleared successfully"
}
```

---

## Complete Usage Example

Here's a complete workflow demonstrating all features:

### 1. Register a token
```bash
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "test-token-abc123", "expiration_seconds": 7200}'
```

### 2. Make some health checks
```bash
# Call /health endpoint a few times
curl http://localhost:5000/health
curl http://localhost:5000/health
curl http://localhost:5000/health
```

### 3. Make some ping requests
```bash
# Call /ping endpoint a few times
curl http://localhost:5000/ping
curl http://localhost:5000/ping
```

### 4. View all persisted requests
```bash
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token-abc123"
```

### 5. Filter by endpoint
```bash
# Get only /health requests
curl "http://localhost:5000/get-responses?endpoint=/health" \
  -H "Authorization: Bearer test-token-abc123"

# Get only /ping requests
curl "http://localhost:5000/get-responses?endpoint=/ping" \
  -H "Authorization: Bearer test-token-abc123"
```

### 6. Limit results
```bash
# Get only the 5 most recent requests
curl "http://localhost:5000/get-responses?limit=5" \
  -H "Authorization: Bearer test-token-abc123"
```

### 7. Clear all responses
```bash
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer test-token-abc123"
```

### 8. Verify responses were cleared
```bash
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token-abc123"
```

Expected response:
```json
{
  "total_returned": 0,
  "redis_connected": true,
  "stats": {
    "connected": true,
    "total_requests": 0,
    "health_requests": 0,
    "ping_requests": 0
  },
  "requests": []
}
```

---

## Token Authentication

### How it works

1. **Token Registration**: Use `/register-token` to register a token in Redis with an expiration time
2. **Token Storage**: Tokens are stored in Redis as `token:<value>` with a TTL (Time To Live)
3. **Token Validation**: The middleware checks if the token exists in Redis before allowing access
4. **Token Expiration**: Tokens automatically expire after the configured time

### Generating Production Tokens

For production use, generate proper JWT tokens:

1. Go to https://www.jwt.io/
2. Create a JWT with your desired payload
3. Copy the generated token
4. Register it using the `/register-token` endpoint

Example JWT payload:
```json
{
  "sub": "user123",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

---

## Error Responses

### Missing Token
```json
{
  "error": "Invalid or missing token",
  "message": "Authorization header is required"
}
```

### Invalid Token Format
```json
{
  "error": "Invalid or missing token",
  "message": "Authorization header must be in format: Bearer <token>"
}
```

### Expired or Invalid Token
```json
{
  "error": "Invalid or missing token",
  "message": "Token is invalid or has expired"
}
```

---

## Docker Compose Usage

For easier deployment, use Docker Compose:

```bash
# Start all services (Redis + App)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down
```

The application will be available at `http://localhost:5000`

---

## Testing

Run the test suite to verify all functionality:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_redis_endpoints.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

All 33 tests should pass, including:
- 5 tests for /health endpoint
- 17 tests for Redis endpoints (including token validation)
- Other service tests

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Token Storage**: In production, use a proper authentication service instead of `/register-token`
2. **HTTPS**: Always use HTTPS in production to protect tokens in transit
3. **Token Rotation**: Implement token rotation for enhanced security
4. **Rate Limiting**: Consider adding rate limiting to prevent abuse
5. **Redis Security**: Secure your Redis instance with passwords and network isolation

---

## Troubleshooting

### Redis Connection Issues

If you see "Redis not available" messages:

1. Verify Redis is running: `docker ps | grep redis`
2. Check connection: `redis-cli ping` (should return "PONG")
3. Verify environment variables are set correctly

### Token Issues

If token validation fails:

1. Verify the token was registered: Check Redis with `redis-cli`
2. Check if token expired: Tokens have TTL set during registration
3. Verify Bearer format: Must be `Authorization: Bearer <token>`

---

## Requirements Met

This implementation fulfills all requirements:

✅ **Redis Database**: Implemented with Docker  
✅ **/health endpoint**: Persists request data to Redis  
✅ **/ping endpoint**: Alternative health check with persistence  
✅ **/get-responses**: Retrieves all persisted requests with filtering  
✅ **/clear-responses**: Deletes all persisted responses  
✅ **Token Validation**: Middleware validates JWT tokens from Redis  
✅ **Selective Protection**: /get-responses and /clear-responses require token, /health does not  
✅ **Token Management**: /register-token endpoint for testing

---

## Additional Resources

- [README.md](README.md) - Project overview and installation
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Comprehensive testing guide
- [JWT.io](https://www.jwt.io/) - JWT token generator
