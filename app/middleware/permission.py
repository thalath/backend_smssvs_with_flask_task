from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def permission_required(permission_code: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    "success": False,
                    "msg": "user not found"
                }), 404
                
            # if not user.is_active:
            #     return jsonify({
            #         "status": 403,
            #         "success": False,
            #         "msg": "User account is inactive."
            #     }), 403
                
            # Check permissions
            if not user.has_permission(permission_code):
                return jsonify({
                    "message": "You do not have permission to perform this action."
                }), 403
                
            return fn(*args, **kwargs)
        return wrapper
    
    return decorator