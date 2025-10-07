from datetime import datetime, timezone

from flask import Flask, jsonify


def create_app():
    """Create Flask app with health endpoint."""
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint for monitoring and CI/CD."""
        return (
            jsonify(
                {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
            ),
            200,
        )

    return app
