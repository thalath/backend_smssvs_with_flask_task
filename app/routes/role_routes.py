from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from ..services import RoleService

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.get("/")
@jwt_required()
def index():
    roles = RoleService.get_all_roles()
    return jsonify({
        "success": True,
        "msg": "roles retrived success",
        "data": [role.to_dict() for role in roles]
    }), 200
    
@role_bp.get("/<int:role_id>")
@jwt_required()
def detail(role_id: int):
    role = RoleService.get_role_by_id(role_id)
    if not role or role is None:
        return jsonify({
            "success": False,
            "msg": f"Role with ID: {role_id} was not found"
        }), 404
        
    return jsonify({
        "msg": "role retrived successfully.",
        "INFO": role.to_dict()
    }), 200
    
    
@role_bp.post("/")
@jwt_required()
def create_role():
    try:
        data = request.get_json()
        if not data:
            jsonify({
                "success": False,
                "msg": "Invalid or Missing JSON payload."
            }), 400
            
        permission = data['permission_ids'] or []
        role = RoleService.create_role(data, permission)
        return jsonify({
            'success': True,
            'msg': 'role created successfully',
            'INFO': role.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An Internal error occured: {str(e)}"
        }), 500
    
@role_bp.put("/<int:role_id>")
@jwt_required()
def edit_role(role_id: int):
    try:
        role = RoleService.get_role_by_id(role_id)
        if role is None:
            return jsonify({
                'success': False,
                'msg': f'role with ID: {role_id} was not found',
            }), 404
            
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                'msg': 'Invalid or Missing JSON payload.'
            }), 400
            
        permission = data['permission_ids'] or []
        new_role = RoleService.update_role(role, data, permission)

        return jsonify({
            'success': False,
            'INFO': new_role.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An Internal error occured: {str(e)}"
        }), 500
    
@role_bp.delete('/<int:role_id>')
@jwt_required()
def delete_role(role_id: int):
    try:
        role = RoleService.get_role_by_id(role_id)
        if role is None:
            return jsonify({
                'success': False,
                'msg': f'Role with ID {role_id} was not found'
            }), 404
            
        return jsonify({
            'success': True,
            'msg': 'role deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": f"An Internal error occured: {str(e)}"
        }), 500