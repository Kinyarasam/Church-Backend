from flask import make_response, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def all_users():
    current_user = get_jwt_identity()
    all_users = storage.all(User).values()
    list_users = [user.to_dict() for user in all_users]
    return make_response(jsonify({"users": list_users}), 200)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    if user_id == 'me':
        user = get_jwt_identity()
        if user:
            user_id = user.get('id', None)
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)
