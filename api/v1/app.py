from flask import Flask, current_app, make_response, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt_request_location
from flask_caching import Cache
from flask_migrate import Migrate
from config import Config
from api.v1.views import app_views
from utils.redis_utils import RedisClient
from api.v1.auth.auth import Auth
import models


app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager()
cache = Cache()
migrate = Migrate(app, models.storage)


@jwt.token_in_blocklist_loader
def validate_jwt_token(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return RedisClient().is_token_blacklisted(jti)


jwt.init_app(app)
cache.init_app(app)
migrate.init_app(app)


app.register_blueprint(app_views)


@app.errorhandler(415)
def notAJSON(error):
    return make_response(jsonify({"error": "Not a JSON"}), 415)


@app.errorhandler(405)
def methodNotAllowed(error):
    return make_response(jsonify({"error": "Method Not Allowed"}), 405)


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({"error": "Not Found!"}), 404)


@app.errorhandler(401)
def Unauthorized(error):
    return make_response(jsonify({"error": "Unauthorized!"}), 401)


@app.errorhandler(400)
def missing(error):
    return make_response(jsonify({"error": "Missing Required Parameters"}), 400)


auth = Auth()


@app.before_request
def before_request():
    setattr(current_app, 'auth', auth)


if __name__ == "__main__":
    app.run(debug=True)
