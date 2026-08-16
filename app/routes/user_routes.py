from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.user_service import UserService

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.get("/")
@jwt_required()
def get_users():
    users = UserService.get_all()
    if users is None:
        return jsonify({
            "error": "users not found"
        }), 404
        
    return jsonify(
        [user.to_dict() for user in users]
    ), 200
    
@user_bp.get("/<int:user_id>")
def get_user_by_id(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "user not found"
        }), 404
        
    return jsonify({
        "msg": "user retrived successfully",
        "INFO": user.to_dict()
    }), 200

@user_bp.post("/")
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({
            "msg": "Body request is required."
        }), 404
        
    users = UserService.create_user(data, data["password"])
    return jsonify({
        "msg": "user created successfully",
        "INFO": users.to_dict()
    }), 201
    
@user_bp.put("/<int:user_id>")
@jwt_required()
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    data = request.get_json()
    if user is None:
        return jsonify({
            "msg": "user not found",
        }), 404
        
    if not data:
        return jsonify({
            "msg": "body request is required!"
        }), 404
    UserService.update_user(user, data)
    return jsonify({
        "msg": "user updated successfully.",
        "info": user.to_dict()
    }), 200
        
    
@user_bp.delete("/<int:user_id>")
@jwt_required()
def delete_user(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        return jsonify({
            "msg": "user not found"
        })
    UserService.delete(user)
    return jsonify({
        "msg": "user deleted successfully"
    }), 200