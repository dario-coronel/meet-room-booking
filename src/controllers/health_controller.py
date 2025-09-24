from datetime import datetime, timezone
from typing import Dict, Any


class HealthController:
    """Controller for health check endpoint following project patterns"""

    @staticmethod
    def get_health_status() -> Dict[str, Any]:
        """
        Get health status of the meet-room-booking service

        Returns:
            Dict containing health status information
        """
        current_time = datetime.now(timezone.utc)

        health_data = {
            "status": "ok",
            "timestamp": current_time.isoformat().replace("+00:00", "Z"),
            "service": "meet-room-booking",
            "version": "1.0.0",
        }

        return health_data

    @staticmethod
    def health_check() -> Dict[str, Any]:
        """
        Health check endpoint handler - returns data for web framework

        Returns:
            Dict with health status and HTTP status code
        """
        try:
            health_status = HealthController.get_health_status()
            return {"data": health_status, "status_code": 200}
        except Exception as e:
            # En caso de error, devolver status degraded pero aún 200
            error_response = {
                "status": "degraded",
                "timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                "service": "meet-room-booking",
                "version": "1.0.0",
                "error": str(e),
            }
            return {"data": error_response, "status_code": 200}
