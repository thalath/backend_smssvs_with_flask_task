from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt, get_jwt_identity
)
from app.models.user import User
from extensions import db
from app.services.user_service import UserService
from app.models.token_blocklist import TokenBlocklist
import re

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/login")
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        if not user.is_active:
            return jsonify({
                "status": 403, 
                "success": False,
                "msg": "you account is inactive, Contact admin to activate."
            }), 403
        token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            "msg": "Logged in successfully",
            "info": user.to_dict(),
            "access_token": token,
            "refresh_token": refresh_token
        }), 200
        
    return jsonify({
        "status": 401,
        "msg": "Invalid email or password"
    }), 401
    
@auth_bp.post("/register")
def register():
    data = request.get_json()
    if not data:
        return jsonify({
            "msg": "body request is required."
        }), 400

    username=data.get("username", "").strip()
    full_name=data.get("full_name", "").strip()
    is_active=data.get("is_active", True)
    email=data.get("email", "").strip()
    password=data.get("password", "")
    confirmation_password=data.get("confirmation_password", "")

    errors: list = []

    if not username:
        errors.append("Username is required.")
    if not full_name:
        errors.append("Full Name is required.")
    if not email:
        errors.append("Email is required.")
    if not password:
        errors.append("Password is required.")

    if password and password != confirmation_password:
        errors.append("Password must be matched.")
        
    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        errors.append("Invalid email formart.")
    
    if not errors:
        existing_username = db.session.scalar(
            db.select(User).filter(User.username==username)
        )
        if existing_username:
            errors.append("Username is already token.")
            
        existing_email = db.session.scalar(
            db.select(User).filter(User.email==email)
        )
        
        if existing_email:
            errors.append("Email is already registered")


    if errors:
        for msg in errors:
            return jsonify({
                "msg": "Validation Fields",
                "errors": msg
            }), 400    
    try:
        user = UserService.create_user(data, data["password"])
        return jsonify({
            "msg": "You are registered. please going to login page.",
            "info": user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print("REGISTER ERROR: ", e)
        import traceback
        traceback.print_exc()
        return jsonify({"msg": f"Internal server error occurred: {e}."}), 500


@auth_bp.post("/logout-access")
@jwt_required()
def logout_access():
    try:
        token_data = get_jwt()
        jti = token_data["jti"]

        blocklisted_token = TokenBlocklist(jti=jti, type="access")
        db.session.add(blocklisted_token)
        db.session.commit()
        return jsonify({"msg": "Access token revoked successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An internal server errors occurred. {e}"})
    
@auth_bp.post("/logout-refresh")
@jwt_required()
def logout_refresh():
    try:
        jti = get_jwt()["jti"]

        block_token = TokenBlocklist(jti=jti, type="refresh")
        db.session.add(block_token)
        db.session.commit()

        return jsonify({"msg": "Refresh token revoked successfully, Full logout complete."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An internal server error occurred: {e}."}), 500
    
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return jsonify({
            "access": access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'msg': f'An Internal error occured: {str(e)}'
        }), 200
        