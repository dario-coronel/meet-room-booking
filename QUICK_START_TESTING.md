# Quick Start Testing Guide

This is a quick reference for testing all the implemented features.

## Prerequisites

1. Start Redis:
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

2. Start the application:
```bash
python run_web.py
```

## Testing Workflow

### Step 1: Test Public Endpoints (No Token Required)

```bash
# Test /health endpoint
curl http://localhost:5000/health

# Test /ping endpoint
curl http://localhost:5000/ping
```

**Expected**: Both should return 200 OK with JSON response

### Step 2: Try Protected Endpoint Without Token (Should Fail)

```bash
# This should return 401 Unauthorized
curl http://localhost:5000/get-responses
```

**Expected Response**:
```json
{
  "error": "Invalid or missing token",
  "message": "Authorization header is required"
}
```

### Step 3: Register a Token

```bash
# Register a test token
curl -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "test-abc123", "expiration_seconds": 3600}'
```

**Expected Response**:
```json
{
  "message": "Token registered successfully",
  "token": "test-abc123",
  "expiration_seconds": 3600
}
```

### Step 4: Access Protected Endpoints With Token

```bash
# Get all persisted requests
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-abc123"
```

**Expected**: Returns all /health and /ping requests that were made

### Step 5: Test Filtering

```bash
# Get only /health requests
curl "http://localhost:5000/get-responses?endpoint=/health" \
  -H "Authorization: Bearer test-abc123"

# Get only 5 most recent requests
curl "http://localhost:5000/get-responses?limit=5" \
  -H "Authorization: Bearer test-abc123"
```

### Step 6: Clear All Responses

```bash
# Clear all persisted data
curl -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer test-abc123"
```

**Expected Response**:
```json
{
  "message": "All responses have been cleared successfully"
}
```

### Step 7: Verify Data Was Cleared

```bash
# Should return empty list
curl http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-abc123"
```

**Expected**: `requests` array should be empty

## Complete Test Script

Save this as `test_all_endpoints.sh`:

```bash
#!/bin/bash

echo "=== Testing Public Endpoints ==="
echo "Testing /health..."
curl -s http://localhost:5000/health | python -m json.tool
echo ""

echo "Testing /ping..."
curl -s http://localhost:5000/ping | python -m json.tool
echo ""

echo "=== Testing Protected Endpoint Without Token (should fail) ==="
curl -s http://localhost:5000/get-responses | python -m json.tool
echo ""

echo "=== Registering Token ==="
curl -s -X POST http://localhost:5000/register-token \
  -H "Content-Type: application/json" \
  -d '{"token": "test-token-xyz", "expiration_seconds": 3600}' | python -m json.tool
echo ""

echo "=== Getting All Responses (with token) ==="
curl -s http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token-xyz" | python -m json.tool
echo ""

echo "=== Filtering by /health endpoint ==="
curl -s "http://localhost:5000/get-responses?endpoint=/health" \
  -H "Authorization: Bearer test-token-xyz" | python -m json.tool
echo ""

echo "=== Limiting to 2 results ==="
curl -s "http://localhost:5000/get-responses?limit=2" \
  -H "Authorization: Bearer test-token-xyz" | python -m json.tool
echo ""

echo "=== Clearing All Responses ==="
curl -s -X DELETE http://localhost:5000/clear-responses \
  -H "Authorization: Bearer test-token-xyz" | python -m json.tool
echo ""

echo "=== Verifying Data Was Cleared ==="
curl -s http://localhost:5000/get-responses \
  -H "Authorization: Bearer test-token-xyz" | python -m json.tool
echo ""

echo "=== All Tests Complete ==="
```

Make it executable and run:
```bash
chmod +x test_all_endpoints.sh
./test_all_endpoints.sh
```

## Running Automated Tests

```bash
# Run all tests
pytest

# Run only Redis endpoint tests
pytest tests/test_redis_endpoints.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

All 33 tests should pass ✅

## Using JWT.io Tokens

1. Go to https://www.jwt.io/
2. Create a JWT token with any payload, for example:
   ```json
   {
     "sub": "1234567890",
     "name": "John Doe",
     "iat": 1516239022
   }
   ```
3. Copy the generated token
4. Register it:
   ```bash
   curl -X POST http://localhost:5000/register-token \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_JWT_TOKEN_HERE", "expiration_seconds": 3600}'
   ```
5. Use it in Authorization header:
   ```bash
   curl http://localhost:5000/get-responses \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

## Docker Compose (Alternative Setup)

Instead of running Redis and the app separately, use Docker Compose:

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop everything
docker-compose down
```

## Endpoints Summary

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/health` | GET | ❌ No | Health check, persists to Redis |
| `/ping` | GET | ❌ No | Ping endpoint, persists to Redis |
| `/register-token` | POST | ❌ No | Register JWT token for testing |
| `/get-responses` | GET | ✅ Yes | Get all persisted requests |
| `/clear-responses` | DELETE | ✅ Yes | Clear all persisted responses |

## Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
docker ps | grep redis

# Test Redis connection
redis-cli ping  # Should return PONG

# Check Redis data
redis-cli
> KEYS *
> LRANGE all_requests 0 -1
```

### Token Issues
```bash
# Check if token exists in Redis
redis-cli
> EXISTS token:your-token-here
> TTL token:your-token-here
```

### Application Not Starting
```bash
# Check if port 5000 is available
lsof -i :5000

# Check Python dependencies
pip install -r requirements.txt

# Check environment variables
echo $REDIS_HOST
echo $REDIS_PORT
```

## Success Criteria

✅ `/health` returns 200 without token
✅ `/ping` returns 200 without token
✅ `/get-responses` returns 401 without token
✅ `/get-responses` returns 200 with valid token
✅ `/clear-responses` returns 401 without token
✅ `/clear-responses` returns 200 with valid token and clears data
✅ All 33 tests pass
✅ No security vulnerabilities (CodeQL scan)

---

**For detailed API documentation, see [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md)**
**For requirements verification, see [REQUIREMENTS_VERIFICATION.md](REQUIREMENTS_VERIFICATION.md)**
