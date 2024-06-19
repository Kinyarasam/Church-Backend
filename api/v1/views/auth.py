from flask import make_response, jsonify, request
from api.v1.views import app_views
from api.v1.services.auth_service import AuthService


@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()
    status = AuthService.register_user(data)
    return make_response(jsonify({"message": status[1]}), status[0])
