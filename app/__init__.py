from flask import Flask, redirect, url_for

from extensions import db, jwt, cors, migrate
from config import Config

def create_app(class_type: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(class_type)
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    from app.models.token_blocklist import check_if_token_is_revoked
    
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.role_routes import role_bp
    from app.routes.permission_routes import perm_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(perm_bp)

    @app.route("/", methods=["GET"])
    def home():
        return redirect(url_for("users.get_users"))
    
    
    from .models.user import User
    from .models.permission import Permission
    from .models.role import Role

    return app