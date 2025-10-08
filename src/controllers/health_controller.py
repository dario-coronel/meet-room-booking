from datetime import datetime, timezone

from flask import Flask, jsonify, request

from src.database.redis_client import redis_client


def create_app():
    app = Flask(__name__)

    @app.route("/clear-responses", methods=["DELETE"])
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

    return app
