from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required

from ..services.permission_service import PermissionService as perm_service

perm_bp = Blueprint("permissions", __name__, url_prefix="/permissions")

@perm_bp.get("/")
@jwt_required()
def index():
    try:
        perms = perm_service.get_all_permissions()
        if not perms:
            return jsonify({
                "success": False,
                "msg": "No permission yet!"
            }), 404
            
        return jsonify({
            "success": True,
            "msg": "Permissions retrived successfully",
            "data": [perm.to_dict() for perm in perms]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An internal occured error: {str(e)}"
        }), 500
    
@perm_bp.get("/<int:perm_id>")
@jwt_required()
def detail(perm_id: int):
    try:
        perm = perm_service.get_permission_by_id(perm_id)
        if perm is None:
            return jsonify({
                "success": False,
                "msg": f"Permission with ID: {perm_id} was not found."
            }), 404
            
        return jsonify({
            "success": True,
            "msg": "Permission retrived successfully.",
            "data": perm.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An internal error occured: {str(e)}"
        }), 500
    
    
@perm_bp.post("/")
@jwt_required()
def create():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "msg": "Invalid or Missing JSON payload."
        }), 400
        
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({
            "success": False,
            "msg": "Validation failed: 'name' field is required and must be a non-empty string"
        }), 422
    
    try:
        perm = perm_service.create_permission(data)
        return jsonify({
            "success": True,
            "msg": "Permission created successfully.",
            "data": perm.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An internal server error occured: {str(e)}"
        }), 500
        
@perm_bp.put("/<int:perm_id>")
@jwt_required()
def edit_permission(perm_id: int):
    perm = perm_service.get_permission_by_id(perm_id)
    if not perm or perm is None:
        return jsonify({
            "success": False,
            "msg": f"No permission with ID: {str(perm_id)}"
        }), 404
        
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "msg": "Invalid or Missing JSON payload."
        }), 400
    try:
        permission = perm_service.update_permission(perm, data)
        return jsonify({
            "success": True,
            "msg": "permission updated successfully.",
            "data": permission.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An internal error occured: {str(e)}"
        }), 500
        

@perm_bp.delete("/<int:perm_id>")
@jwt_required()
def delete_permission(perm_id: int):
    perm = perm_service.get_permission_by_id(perm_id)
    if not perm or perm is None:
        return jsonify({
            "suceces": False,
            "msg": f"Permission with ID: {perm_id} was not found."
        }), 404
        
    try:
        perm_service.delete_permission(perm)
        return jsonify({
            "success": True,
            "msg": "Permission deleted successfully."
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An Internal error occured: {str(e)}"
        }), 500