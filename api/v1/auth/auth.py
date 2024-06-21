from models.user import User
from flask_jwt_extended import get_jwt
from utils.redis_utils import RedisClient


class Auth:
    def authorization_header(self, request=None) -> str:
        if request is None:
            return
        return request.headers.get('Authorization', None)
    
    def current_user(self, request=None) -> User:
        pass
    
    def blacklist_jwt(self):
        jti = get_jwt()['jti']
        RedisClient().add_to_blacklist(jti)
        
