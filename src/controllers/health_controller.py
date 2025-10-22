from datetime import datetime, timezone

from flask import Flask, jsonify, request

from src.database.redis_client import redis_client
from src.middleware.auth_middleware import validate_token


def create_app():
    app = Flask(__name__)

    @app.route("/clear-responses", methods=["DELETE"])
    @validate_token
    def clear_responses():
        """Elimina todas las respuestas persistidas en Redis o base de datos."""
        success = redis_client.clear_all_requests()
        if success:
            return (
                jsonify({"message": "All responses have been cleared successfully"}),
                200,
            )
        else:
            return jsonify({"message": "Failed to clear responses"}), 500

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint for monitoring and CI/CD.

        Persists request information to Redis for monitoring.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Get request info
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent")

        # Save to Redis
        redis_client.save_request(
            endpoint="/health",
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data={"response_status": "ok"},
        )

        return (
            jsonify({"status": "ok", "timestamp": timestamp}),
            200,
        )

    @app.route("/ping", methods=["GET"])
    def ping():
        """Ping endpoint to verify service availability.

        Similar to /health but with explicit 'pong' response.
        Also persists request information to Redis.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Get request info
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent")

        # Save to Redis
        redis_client.save_request(
            endpoint="/ping",
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data={"response": "pong"},
        )

        return (
            jsonify(
                {
                    "status": "pong",
                    "timestamp": timestamp,
                    "message": "Service is alive",
                }
            ),
            200,
        )

    @app.route("/get-responses", methods=["GET"])
    @validate_token
    def get_responses():
        """Get all persisted requests from Redis.

        Returns all stored health check and ping requests with metadata.
        """
        # Get query parameters
        endpoint = request.args.get("endpoint")  # Optional filter
        limit = int(request.args.get("limit", 100))  # Default 100

        if endpoint:
            requests_data = redis_client.get_requests_by_endpoint(endpoint, limit)
        else:
            requests_data = redis_client.get_all_requests(limit)

        stats = redis_client.get_stats()

        return (
            jsonify(
                {
                    "total_returned": len(requests_data),
                    "redis_connected": redis_client.is_connected(),
                    "stats": stats,
                    "requests": requests_data,
                }
            ),
            200,
        )

    @app.route("/register-token", methods=["POST"])
    def register_token():
        """Registra un token JWT en Redis para testing.

        Espera un JSON con el campo 'token' y opcionalmente 'expiration_seconds'.
        Ejemplo:
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "expiration_seconds": 3600
        }
        """
        data = request.get_json()

        if not data or "token" not in data:
            return (
                jsonify(
                    {
                        "error": "Token is required",
                        "message": "Please provide a 'token' field in the request body",
                    }
                ),
                400,
            )

        token = data["token"]
        expiration = data.get("expiration_seconds", 3600)  # Default: 1 hora

        success = redis_client.save_token(token, expiration)

        if success:
            return (
                jsonify(
                    {
                        "message": "Token registered successfully",
                        "token": token,
                        "expiration_seconds": expiration,
                    }
                ),
                201,
            )
        else:
            return (
                jsonify(
                    {
                        "error": "Failed to register token",
                        "message": "Redis connection error",
                    }
                ),
                500,
            )

    return app
