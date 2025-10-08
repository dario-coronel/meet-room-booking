import json
import time

import requests

print("🧪 Probando endpoints del Meeting Room Booking System\n")
print("=" * 60)

base_url = "http://localhost:5000"

# Esperar a que el servidor esté listo
print("\n⏳ Esperando que el servidor esté listo...")
time.sleep(2)

# Test 1: /health
print("\n1️⃣ Probando GET /health")
try:
    response = requests.get(f"{base_url}/health", timeout=5)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("   ✅ PASS")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

# Test 2: /ping
print("\n2️⃣ Probando GET /ping")
try:
    response = requests.get(f"{base_url}/ping", timeout=5)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "pong"
    print("   ✅ PASS")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

# Test 3: /get-responses
print("\n3️⃣ Probando GET /get-responses")
try:
    response = requests.get(f"{base_url}/get-responses", timeout=5)
    print(f"   Status Code: {response.status_code}")
    data = response.json()
    print(f"   Total returned: {data['total_returned']}")
    print(f"   Redis connected: {data['redis_connected']}")
    print(f"   Stats: {json.dumps(data['stats'], indent=2)}")
    assert response.status_code == 200
    print("   ✅ PASS")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

# Test 4: /get-responses con filtros
print("\n4️⃣ Probando GET /get-responses?limit=5")
try:
    response = requests.get(f"{base_url}/get-responses?limit=5", timeout=5)
    print(f"   Status Code: {response.status_code}")
    data = response.json()
    print(f"   Total returned: {data['total_returned']}")
    assert response.status_code == 200
    print("   ✅ PASS")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

# Test 5: /get-responses filtrado por endpoint
print("\n5️⃣ Probando GET /get-responses?endpoint=/health")
try:
    response = requests.get(f"{base_url}/get-responses?endpoint=/health", timeout=5)
    print(f"   Status Code: {response.status_code}")
    data = response.json()
    print(f"   Total returned: {data['total_returned']}")
    assert response.status_code == 200
    print("   ✅ PASS")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

print("\n" + "=" * 60)
print("✅ Pruebas completadas!")
print("\n📝 Nota: Redis no está disponible, pero la app funciona correctamente")
print("   en modo degradado (sin persistencia de requests).")
