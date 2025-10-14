"""Middleware para validación de tokens JWT."""

from functools import wraps

from flask import jsonify, request

from src.database.redis_client import redis_client


def validate_token(f):
    """Middleware que valida el token JWT en el header Authorization.

    Verifica que:
    1. El header Authorization esté presente
    2. Tenga el formato: Bearer <token>
    3. El token exista en Redis (token:<valor>)

    Si falla alguna validación, retorna 401 Unauthorized.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el header Authorization
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return (
                jsonify(
                    {
                        "error": "Invalid or missing token",
                        "message": "Authorization header is required",
                    }
                ),
                401,
            )

        # Verificar formato: Bearer <token>
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return (
                jsonify(
                    {
                        "error": "Invalid or missing token",
                        "message": (
                            "Authorization header must be in format: " "Bearer <token>"
                        ),
                    }
                ),
                401,
            )

        token = parts[1]

        # Validar token en Redis
        if not redis_client.validate_token(token):
            return (
                jsonify(
                    {
                        "error": "Invalid or missing token",
                        "message": "Token is invalid or has expired",
                    }
                ),
                401,
            )

        # Token válido, permitir acceso
        return f(*args, **kwargs)

    return decorated_function
