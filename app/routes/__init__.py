from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from .role_routes import role_bp

__all__ = [
    "user_bp", "auth_bp", 'role_bp'
]