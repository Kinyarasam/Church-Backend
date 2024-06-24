from flask import Flask, current_app, session, make_response, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt_request_location
from flask_caching import Cache
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import Config
from api.v1.views import app_views
from utils.redis_utils import RedisClient
from api.v1.auth.auth import Auth
import models

socketio = SocketIO(logger=True, engineio_logger=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db = models.storage
    jwt = JWTManager()
    cache = Cache()
    migrate = Migrate(app, db)


    @jwt.token_in_blocklist_loader
    def validate_jwt_token(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RedisClient().is_token_blacklisted(jti)


    jwt.init_app(app)
    cache.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app)


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

    import api.v1.services.chat_services
        
    @app.route('/', methods=['GET'])
    def hello():
        return "Welcome"
    
    @app.route('/session')
    def session_route():
        session['foo'] = 'bar'
        setattr(session, 'foo', 'bar')
        print(session.__dict__)
        return ''

    # import api.v1.services.chat_services
    
    # setattr(app, 'socketio', socketio)
    
    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
