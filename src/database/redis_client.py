import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import redis


class RedisClient:
    def clear_all_requests(self) -> bool:
        """Elimina todas las respuestas persistidas en Redis."""
        if not self.is_connected():
            return False
        try:
            # Eliminar lista general
            self.client.delete("all_requests")
            # Eliminar sets de endpoints conocidos
            self.client.delete("requests:/health")
            self.client.delete("requests:/ping")
            # Si hay más endpoints, podrías usar scan y delete por patrón
            return True
        except Exception as e:
            print(f"Error clearing requests in Redis: {e}")
            return False

    """Redis client for storing health check and ping requests."""

    def __init__(self):
        """Initialize Redis connection."""
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))

        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            # Test connection
            self.client.ping()
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Warning: Redis not available: {e}")
            self.client = None

    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        if self.client is None:
            return False
        try:
            self.client.ping()
            return True
        except (redis.ConnectionError, redis.TimeoutError):
            return False

    def save_request(
        self,
        endpoint: str,
        ip_address: str,
        user_agent: Optional[str] = None,
        additional_data: Optional[Dict] = None,
    ) -> str:
        """Save request information to Redis.

        Args:
            endpoint: The endpoint that was called
            ip_address: IP address of the requester
            user_agent: User agent string
            additional_data: Any additional data to store

        Returns:
            The key used to store the data
        """
        if not self.is_connected():
            return None

        timestamp = datetime.utcnow().isoformat()
        request_id = f"{endpoint}:{timestamp}"

        data = {
            "endpoint": endpoint,
            "ip_address": ip_address,
            "user_agent": user_agent or "unknown",
            "timestamp": timestamp,
            "additional_data": additional_data or {},
        }

        try:
            # Store in a sorted set with timestamp as score
            key = f"requests:{endpoint}"
            self.client.zadd(key, {json.dumps(data): datetime.utcnow().timestamp()})

            # Also store in a list for easy retrieval
            self.client.lpush("all_requests", json.dumps(data))

            return request_id
        except Exception as e:
            print(f"Error saving to Redis: {e}")
            return None

    def get_all_requests(self, limit: int = 100) -> List[Dict]:
        """Get all stored requests.

        Args:
            limit: Maximum number of requests to return

        Returns:
            List of request dictionaries
        """
        if not self.is_connected():
            return []

        try:
            # Get from list
            raw_requests = self.client.lrange("all_requests", 0, limit - 1)
            requests = [json.loads(req) for req in raw_requests]
            return requests
        except Exception as e:
            print(f"Error retrieving from Redis: {e}")
            return []

    def get_requests_by_endpoint(self, endpoint: str, limit: int = 100) -> List[Dict]:
        """Get requests for a specific endpoint.

        Args:
            endpoint: The endpoint to filter by
            limit: Maximum number of requests to return

        Returns:
            List of request dictionaries
        """
        if not self.is_connected():
            return []

        try:
            key = f"requests:{endpoint}"
            # Get from sorted set (most recent first)
            raw_requests = self.client.zrevrange(key, 0, limit - 1)
            requests = [json.loads(req) for req in raw_requests]
            return requests
        except Exception as e:
            print(f"Error retrieving from Redis: {e}")
            return []

    def get_stats(self) -> Dict:
        """Get statistics about stored requests.

        Returns:
            Dictionary with stats
        """
        if not self.is_connected():
            return {"connected": False}

        try:
            total_requests = self.client.llen("all_requests")
            health_requests = self.client.zcard("requests:/health")
            ping_requests = self.client.zcard("requests:/ping")

            return {
                "connected": True,
                "total_requests": total_requests,
                "health_requests": health_requests,
                "ping_requests": ping_requests,
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"connected": False, "error": str(e)}


# Global Redis client instance
redis_client = RedisClient()
