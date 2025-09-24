from datetime import datetime, timezone

from flask import Flask, jsonify


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Health endpoint - Required by TP
    @app.route("/health", methods=["GET"])
    def health_check():
        """
        Health check endpoint to verify service is running.

        Returns:
            JSON response with status 'ok' and current timestamp
            Status code: 200
        """
        return (
            jsonify(
                {
                    "status": "ok",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            200,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
