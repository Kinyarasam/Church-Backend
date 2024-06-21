from flask import make_response, jsonify, request, abort, current_app
from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.services.auth_service import AuthService


@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()
    status = AuthService.register_user(data)
    return make_response(jsonify({"message": status[1]}), status[0])


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    response = AuthService.login(data)
    return make_response(jsonify({'message': response[1]}), response[0])

@app_views.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    auth = current_app.auth
    auth.blacklist_jwt()
    return make_response(jsonify({"message": "Logged Out"}), 201)
