# from flask import Blueprint, jsonify

# error_bp = Blueprint("errors", __name__, url_prefix="/errors")

# @error_bp.errorhandler(403)
# def forbidden_error(error):
#     return jsonify({
#         "success": False,
#         "status": 403,
#         "msg": getattr(str(error), "description", "Access denied.")
#     }), 403